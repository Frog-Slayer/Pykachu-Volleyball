import gymnasium
import numpy as np
import time
import pykachu_physics

class PykachuEnv(gym.env):
    metadata = {'render.modes': ['human']}

    def __init__(self, isPlayer1Computer, isPlayer2Computer):
        pykachu_physics.PikaPhysics(self, isPlayer1Computer, isPlayer2Computer)
        return

    def step(self, userInputArray):
        isBallTouchingGround = pykachu_physics.physicsEngine(self.player1, self.player2, self.ball, userInputArray)
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

        return observation, 0, False, {}

    def render(self):
        pass        
        return



    def reset(self, isPlayer2Serve):
        self.player1.initializeForNewRound()
        self.player2.initializeForNewRound()
        self.ball.initializeForNewRound(isPlayer2Serve)
        obs_p1 = [self.ball.x, self.ball.xVelocity, self.ball.y, self.ball.yVelocity,
                  self.player1.x, self.player1.y, self.player2.x, self.player2.y]
        obs_p2 = [self.ball.x, self.ball.xVelocity, self.ball.y, self.ball.yVelocity,
                  self.player1.x, self.player1.y, self.player2.x, self.player2.y]
        observation = (obs_p1, obs_p2)
        return 
    
    