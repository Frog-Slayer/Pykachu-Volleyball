import gymnasium as gym
import numpy as np
from pykachu_volleyball_env import PykachuEnv

env = PykachuEnv()
env.render_mode = 'human'

is_player_2_serve = False

for episode in range(4):
    env.reset(is_player_2_serve = is_player_2_serve)

    while True:
        env.render()
        action = env.action_space.sample()
        state, reward, done, info = env.step(action)
        print(info)

        if done:
            if reward == 1:
                is_player_2_serve = False
            else:
                is_player_2_serve = True
            break

env.close()
