import gymnasium as gym
import numpy as np
import pygame

from gymnasium.spaces import MultiDiscrete, Box

import pykachu_physics
from constants import (
    GROUND_HEIGHT, GROUND_WIDTH, GROUND_HALF_WIDTH
)
from pykachu_render import GameViewDrawer
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
        return

    @property
    def observation(self):
        pixels = pygame.surfarray.pixels3d(self._surface)
        return np.transform(np.array(pixels), axes=(1, 0, 2))

    def step(self, action):
        isBallTouchingGround = self.physics.runEngineForNextFrame(action)
        
        if isBallTouchingGround:
            if self.physics.ball.punchEffectX < GROUND_HALF_WIDTH:
                self.isPlayer2Serve = True
                self.reward = -1
            else:
                self.isPlayer2Serve = False
                self.reward = 1

            self.terminated = True
        else:
            self.reward = 0


        return self.observation, self.reward, self.terminated


    def render(self):
        if self._surface is None:
            pygame.init()

            if self.render_mode == 'human':
                pygame.display.init()
                pygame.display.set_mode((GROUND_WIDTH, GROUND_HEIGHT))
                pygame.display.set_caption('Pykachu Volleyball')
                self.gameView = GameViewDrawer()

            elif self.render_mode == "rgb_array":
                return self.observation
            
        # Draw
        if self.render_mode == 'human':
            self.gameView.draw_players_and_ball(self.physics) 

    def reset(self, seed):
        super().reset(seed = seed)

        return self.observation
    