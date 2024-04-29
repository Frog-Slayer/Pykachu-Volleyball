import gymnasium as gym
import numpy as np
import time
import pygame
import pykachu_physics
from pykachu_render import GameViewDrawer
from pykachu_physics import PikaPhysics

class PykachuEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, isPlayer1Computer, isPlayer2Computer):
        self.physics = PikaPhysics(isPlayer1Computer, isPlayer2Computer)
        return

    def step(self, action):
        isBallTouchingGround = self.physics.runEngineForNextFrame(self.player1, self.player2, self.ball, action)

        obs_p1 = [self.ball.x, self.ball.xVelocity, self.ball.y, self.ball.yVelocity,
                  self.player1.x, self.player1.y, self.player2.x, self.player2.y]

        obs_p2 = [self.ball.x, self.ball.xVelocity, self.ball.y, self.ball.yVelocity,
                  self.player1.x, self.player1.y, self.player2.x, self.player2.y]
        observation = (obs_p1, obs_p2)
        
        if (isBallTouchingGround):
            if (self.ball.x < pykachu_physics.GROUND_HALF_WIDTH):
                return observation, 1, True, {}
            else:
                return observation, -1, True, {}

        if self.render_mode == "human":
            self.render()

        return observation, 0, False, {}

    def render(self):
        if self._surface is None:
            pygame.init()

            if self.render_mode == 'human':
                pygame.display.init()
                pygame.display.set_caption('Pykachu Volleyball')
                self.gameView = GameViewDrawer()

            elif self.render_mode == "rgb_array":
                return self.observation
            
        # Draw
        if self.render_mode == 'human':
            self.gameView.draw_players_and_ball(self.physics) 

    def reset(self, seed):
        super().reset(seed = seed)

        ball = self.physics.ball
        player1 = self.physics.player1
        player2 = self.physics.player2

        obs_p1 = [ball.x, ball.xVelocity, ball.y, ball.yVelocity,
                  player1.x, player1.y, player2.x, player2.y]

        obs_p2 = [ball.x, ball.xVelocity, ball.y, ball.yVelocity,
                  player1.x, player1.y, player2.x, player2.y]

        observation = (obs_p1, obs_p2)

        return observation 
    
    