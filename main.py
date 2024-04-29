import gymnasium as gym
import pygame
import numpy as np
from gymnasium.utils.play import play

import pykachu_env

env = pykachu_env.PykachuEnv(False, False)
env.render_mode = 'rgb_array'
play(env, keys_to_action={(pygame.K_SPACE,): np.array([1])}, noop=np.array([0]),
     fps=24)