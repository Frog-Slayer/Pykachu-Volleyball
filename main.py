import gymnasium as gym
import pygame
from gymnasium.utils.play import play

import pykachu_env

env = pykachu_env.PykachuEnv(False, False)
env.render_mode = 'human'