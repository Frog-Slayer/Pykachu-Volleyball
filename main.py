import gymnasium as gym
import numpy as np
from gymnasium.utils.play import play

import pykachu_env

env = pykachu_env.PykachuEnv(False, False)
env.render_mode = 'human'

for episode in range(2):
    env.reset()
    for step in range(500):
        env.render()
        action = env.action_space.sample()
        state, reward, done, info = env.step(action)
        if done:
            break

env.close()
