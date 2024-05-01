# Pykachu-Volleyball

(대충 사진)

# Introduction
The source code on this repository is an adaption of [the code](https://github.com/gorisanson/pikachu-volleyball), which is gained by reverse engineering the original game, developed by "(C) SACHI SOFT"

This is a `gymnasium` environment for single-agent reinforcement learning with a computer as an opponent. Multi-agent environment will be added later, using `pettingzoo`.


# Description
 
```python
#this is in sample.py
import gymnasium as gym
import pykachu_env

env = gym.make('PykachuVolleyball-v0', 
               render_mode= "human", 
               is_player_2_computer=False)
```





|                   |                          |
|-------------------|--------------------------|
| Action Space      | MultiDiscrete([3, 3, 1]) |
| Observation Space | (432, 304, 3)            |
| Observation High  | 255                      |
| Observation Low   | 0                        |


## Action Space
The action space is `MultiDiscrete([3, 3, 1])`, and each corresponds to left-right input, up-down input, and power hit input in order.

### `action_space[0]` (left-right movement)
| Value             | Meaning                  |
|-------------------|--------------------------|
| 0                 | input left movement      |
| 1                 | NOOP                     |
| 2                 | input right movement     |

### `action_space[1]` (up-down movement)
| Value             | Meaning                  |
|-------------------|--------------------------|
| 0                 | input up movement        |
| 1                 | NOOP                     |
| 2                 | input down movement      |

### `action_space[2]` (power hit)
| Value             | Meaning                  |
|-------------------|--------------------------|
| 0                 | NOOP                     |
| 1                 | input power hit          |


## Observation Space
The observation space is `Box(low=0, high=255, shape=(432, 304, 3), dtype=np.uint8)`. It is the RGB image, displayed to a human player. 

```python
#this is in sample.py
for episode in range(5):
    env.reset()

    while True:
        env.render()
        action = env.action_space.sample()
        state, reward, terminated, info = env.step(action)
        if terminated:
            break

env.close()
```

The `step()` funcion also returns `reward`, `terminated`, and `info`, along with the above `observation`. 

### `reward`
You'll get `+1` when you win, otherwise `-1`(i.e. if the opponent computer wins).

### `terminated`
`True` if the ball touches the ground, otherwise `False`. 

### `info`
You can get additional information about the players and tha ball.
```json
{
    "player1": {
        "x": player1.x,
        "y": player1.y,
        "dive_direction" : player1.dive_direction 
    },
    "player2":{
        "x": player2.x,
        "y": player2.y,
        "dive_direction" : player2.dive_direction 
    },
    "ball": {
        "x": ball.x,
        "x_velocity": ball.x_velocity,
        "y": ball.y,
        "y_velocity": ball.y_velocity,
    }
}
```


# TODOs
For the code may not be fully compliant with `gymnasium` standard APIs, there may be some bugs or issues. Please let me know if there is an error or if you need additional functions. Good luck.

- [X] reset and reward 
- [X] refactor to Python convention 
- [X] draw background
- [X] ~~show game start message~~
- [X] transparent Pikachu background 
- [X] trail, punch, hyper sprites 
- [X] fix computer's improper movements
- [X] ball rotation 
- [X] draw shadows
- [ ] support render_mode 'rgb_array'
- [ ] specific comments 
- [ ] add sound(and make it optional) 