import gymnasium as gym
import pygame
import numpy as np
from gymnasium.utils.play import play

import pykachu_env

env = pykachu_env.PykachuEnv(True, False)
env.render_mode = 'human'


for i in range(20):
    observation = env.reset()