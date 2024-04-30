import gymnasium as gym
import numpy as np
from pykachu_volleyball_env import PykachuEnv

env = PykachuEnv(isPlayer1Computer= True, isPlayer2Computer= True)
env.render_mode = 'human'

isPlayer2Serve = False

for episode in range(4):
    env.reset(isPlayer2Serve = isPlayer2Serve)

    while True:
        env.render()
        action = env.action_space.sample()
        state, reward, done, info = env.step(action)
        print(info)

        if done:
            if reward == 1:
                isPlayer2Serve = False
            else:
                isPlayer2Serve = True
            break

env.close()
