import gymnasium as gym
from pykachu_volleyball_env import PykachuEnv

"""
This is a sample code
"""
env = PykachuEnv(is_player_2_computer=True)
env.render_mode = 'human'

for episode in range(50):
    env.reset()

    while True:
        env.render()
        action = env.action_space.sample()
        state, reward, done, info = env.step(action)
        if done:
            break

env.close()
