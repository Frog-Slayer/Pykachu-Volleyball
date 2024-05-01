import gymnasium as gym
from pykachu_volleyball_env import PykachuEnv

env = PykachuEnv(is_player_2_computer=False)
env.render_mode = 'human'

is_player_2_serve = False

for episode in range(4):
    env.reset()

    while True:
        env.render()
        action = env.action_space.sample()
        state, reward, done, info = env.step(action)
        print(info)

        if done:
            break

env.close()
