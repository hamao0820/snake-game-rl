import sys
from typing import Generic, Literal, Tuple, TypeAlias, TypeVar

sys.path.append("./src/websocketClient")
from websocket_client import Action, WebsocketClient

Action_Space: TypeAlias = Tuple[Literal[0], Literal[1], Literal[2]]
ObsType = TypeVar("ObsType")


class SnakeGameEnv(Generic[ObsType]):
    def __init__(self) -> None:
        self.client = WebsocketClient()
        self.__action_space: Action_Space = (0, 1, 2)
        self.client.connect()
        pass

    def reset(self) -> Tuple[ObsType, dict]:
        state, info = self.client.reset()
        return state, info

    def step(self, action: Action) -> Tuple[ObsType, float, bool, bool, dict]:
        observation, reward, terminated, truncated, info = self.client.step(action)
        return observation, reward, terminated, truncated, info

    def close(self) -> None:
        self.client.close()

    @property
    def action_space(self) -> Action_Space:
        return self.__action_space


# env = SnakeGameEnv[str]()
# state, info = env.reset()
# print(state)
# print(info)

# while True:
#     action = env.action_space[0]
#     observation, reward, terminated, truncated, info = env.step(action)
#     print(observation)
#     print(reward)
#     print(terminated)
#     print(truncated)
#     print(info)
#     if terminated:
#         print("terminated")
#         env.close()
#         break
