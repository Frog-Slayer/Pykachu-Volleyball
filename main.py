import gymnasium as gym
import pygame
import numpy as np
from gymnasium.utils.play import play

import pykachu_env

env = pykachu_env.PykachuEnv(False, False)
env.render_mode = 'human'

for _ in range(300):
    env.render()
    action = env.action_space.sample()
    state, reward, done, info = env.step(action)
    print(info)

env.close()