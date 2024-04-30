import gymnasium as gym
import numpy as np
import pygame

from gymnasium.spaces import MultiDiscrete, Box
import pykachu_physics

from constants import (
    GROUND_HEIGHT, GROUND_WIDTH, GROUND_HALF_WIDTH
)

from pykachu_render import GameViewDrawer, Texture
from pykachu_physics import PikaPhysics

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

    def __init__(self, isPlayer1Computer, isPlayer2Computer):
        self.physics = PikaPhysics(isPlayer1Computer, isPlayer2Computer)
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
                "divingDirection" : player1.divingDirection 
            },
            "player2":{
                "x": player2.x,
                "y": player2.y,
                "divingDirection" : player2.divingDirection 
            },
            "ball": {
                "x": ball.x,
                "xVelocity": ball.xVelocity,
                "y": ball.y,
                "yVelocity": ball.yVelocity,
            }
        }

    def step(self, action):
        userInput = pykachu_physics.PikaUserInput(action)
        cpuInput = pykachu_physics.PikaUserInput()

        isBallTouchingGround = self.physics.runEngineForNextFrame([userInput, cpuInput])
        terminated = False 
        if isBallTouchingGround:
            if self.physics.ball.punchEffectX < GROUND_HALF_WIDTH:
                self.isPlayer2Serve = True
                self.reward = -1
            else:
                self.isPlayer2Serve = False
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
                self.gameView = GameViewDrawer(self.texture)

            elif self.render_mode == "rgb_array":
                return self.observation
            
        # Draw
        if self.render_mode == 'human':
            pygame.event.pump()
            self._surface.fill((0, 0, 0))
            self.gameView.drawBackground()
            self.gameView.draw_players_and_ball(self.physics) 
            pygame.display.update()
            self.clock.tick(25)

    def reset(self, seed):
        super().reset(seed = seed)

        return self.observation
    