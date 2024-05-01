import gymnasium as gym
import pykachu_env

env = gym.make('PykachuVolleyball-v0', 
               render_mode= "human", 
               is_player_2_computer=False)

for episode in range(50):
    env.reset()

    while True:
        env.render()
        action = env.action_space.sample()
        state, reward, terminated, info = env.step(action)
        if terminated:
            break

env.close()