import gymnasium as gym
import numpy as np
from pykachu_volleyball_env import PykachuEnv

env = PykachuEnv(False, True)
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
