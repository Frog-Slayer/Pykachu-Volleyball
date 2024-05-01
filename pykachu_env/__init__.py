from .pykachu_volleyball_env import PykachuEnv
from gymnasium.envs.registration import register

__all__ = [PykachuEnv]
register(id="PykachuVolleyball-v0", entry_point="pykachu_env:PykachuEnv")