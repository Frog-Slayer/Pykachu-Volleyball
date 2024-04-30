import gymnasium as gym
import numpy as np
import pygame

from gymnasium.spaces import MultiDiscrete, Box
import physics

from constants import (
    GROUND_HEIGHT, GROUND_WIDTH, GROUND_HALF_WIDTH
)

from render import GameViewDrawer, Texture
from physics import PykaPhysics

"""
RL environment for 'single' agent. The opponent is the basic AI, originally implemented in the game.
Multi-agent environment using pettingzoo will be added later
"""
class PykachuEnv(gym.Env):
    action_space = MultiDiscrete([3, 3, 1]) 
    """
    (none, up, down), (node, left, right), (none, power hit)
    """
    
    observation_space = Box(low = 0, high = 255, shape=(GROUND_WIDTH, GROUND_HEIGHT, 3),
                            dtype=np.uint8)
    """
    The Space object for all valid observations, corresponding to rendered display of the game(in RGB)
    """                        

    metadata = {'render.modes': ['human']}
    """
    metadata for the environment containing rendering modes, etc 
    """

    def __init__(self):
        self.physics = PykaPhysics()
        self._surface = None
        self.clock = pygame.time.Clock()
        return

    @property
    def observation(self):
        pixels = pygame.surfarray.pixels3d(self._surface)
        return np.transpose(np.array(pixels), axes=(1, 0, 2))

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
        user_input = physics.UserInput(action)
        cpu_input = physics.UserInput()

        is_ball_touching_ground = self.physics.run_engine([user_input, cpu_input])
        terminated = False 
        if is_ball_touching_ground:
            if self.physics.ball.punch_effect_x < GROUND_HALF_WIDTH:
                self.is_player_2_serve = True
                self.reward = -1
            else:
                self.is_player_2_serve = False
                self.reward = 1

            terminated = True
        else:
            self.reward = 0

        return self.observation, self.reward, terminated, self.info


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
            self.clock.tick(25)

    def reset(self, seed = None, is_player_2_serve = False):
        super().reset(seed = seed)

        self.physics.reset(is_player_2_serve)

        if self.render_mode is not None:
            self.render()

        return self.observation
    