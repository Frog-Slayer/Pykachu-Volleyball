import gymnasium as gym
import pygame
import numpy as np
from gymnasium.utils.play import play

import pykachu_env

env = pykachu_env.PykachuEnv(False, False)
env.render_mode = 'human'

for _ in range(100):
    env.render()
    action = env.action_space.sample()
    state, reward, done = env.step(action)

env.close()