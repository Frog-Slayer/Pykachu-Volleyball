import gymnasium as gym
import numpy as np
import pygame

from gymnasium.spaces import MultiDiscrete, Box

from .constants import (
    GROUND_HEIGHT, GROUND_WIDTH, GROUND_HALF_WIDTH
)

from .render import GameViewDrawer, Texture
from .physics import PykaPhysics, UserInput

"""
RL environment for 'single' agent. The opponent is the basic AI, originally implemented in the game.
Multi-agent environment using pettingzoo will be added later
"""
class PykachuEnv(gym.Env):
    action_space = MultiDiscrete([3, 3, 2]) 
    """
    (node, left, right), (none, up, down), (none, power hit)
    """
    
    observation_space = Box(low = 0, high = 255, shape=(GROUND_WIDTH, GROUND_HEIGHT, 3),
                            dtype=np.uint8)
    """
    The Space object for all valid observations, corresponding to rendered display of the game(in RGB)
    """                        

    metadata = {'render_modes': ['human']}
    """
    metadata for the environment containing rendering modes, etc 
    """

    def __init__(self, is_player_2_computer= False, render_mode= None):
        self.render_mode = render_mode
        self.physics = PykaPhysics(is_player_2_computer)
        self._surface = None
        self._clock = pygame.time.Clock()
        self.is_player_2_computer = is_player_2_computer
        self.is_player_2_serve = False
        return

    @property
    def observation(self):
        pixels = pygame.surfarray.pixels3d(self._surface)
        return np.transpose(np.array(pixels), axes=(1, 0, 2))

    @property
    def reward(self):
        if self.is_ball_touching_ground:
            if self.physics.ball.punch_effect_x < GROUND_HALF_WIDTH: #player2 wins
                self.is_player_2_serve = True
                return -1 if self.is_player_2_computer else 1
            else:#player1 wins
                self.is_player_2_serve = False
                return 1 if self.is_player_2_computer else 1
        else:
            return 0


    @property
    def terminated(self):
        return self.is_ball_touching_ground

    @property
    def info(self):
        player1 = self.physics.player1
        player2 = self.physics.player2
        ball = self.physics.ball
        return {
            "player1": {
                "x": player1.x,
                "y": player1.y,
                "dive_direction" : player1.dive_direction 
            },
            "player2":{
                "x": player2.x,
                "y": player2.y,
                "dive_direction" : player2.dive_direction 
            },
            "ball": {
                "x": ball.x,
                "x_velocity": ball.x_velocity,
                "y": ball.y,
                "y_velocity": ball.y_velocity,
            }
        }

    def step(self, action):
        player1_input = UserInput(action)
        player2_input = UserInput(action)

        self.is_ball_touching_ground = self.physics.run_engine([player1_input, player2_input])

        if self.is_ball_touching_ground:
            if self.physics.ball.punch_effect_x < GROUND_HALF_WIDTH: #player2 wins
                self.is_player_2_serve = True
            else:#player1 wins
                self.is_player_2_serve = False
 
        return self.observation, self.reward, self.terminated, self.info


    def render(self):
        if self._surface is None:
            pygame.init()

            if self.render_mode == 'human':
                pygame.display.init()
                self._surface = pygame.display.set_mode((GROUND_WIDTH, GROUND_HEIGHT))
                pygame.display.set_caption('Pykachu Volleyball')
                self.texture = Texture()
                self.view = GameViewDrawer(self.texture)

            elif self.render_mode == "rgb_array":
                return self.observation
            
        # Draw
        if self.render_mode == 'human':
            pygame.event.pump()
            self.view.draw_background()
            self.view.draw_players_and_ball(self.physics) 
            pygame.display.update()
            self._clock.tick(25)

    def reset(self, seed = None):
        super().reset(seed = seed)

        self.physics.reset(self.is_player_2_serve)

        if self.render_mode is not None:
            self.render()

        return self.observation
    