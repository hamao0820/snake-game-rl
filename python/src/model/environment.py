import asyncio
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
        asyncio.set_event_loop(asyncio.new_event_loop())
        asyncio.get_event_loop().run_until_complete(self.client.connect())
        pass

    def reset(self) -> Tuple[ObsType, dict]:
        state, info = asyncio.get_event_loop().run_until_complete(self.client.reset())
        return state, info

    def step(self, action: Action) -> Tuple[ObsType, float, bool, bool, dict]:
        observation, reward, terminated, truncated, info = asyncio.get_event_loop().run_until_complete(
            self.client.step(action)
        )
        return observation, reward, terminated, truncated, info

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
#         break
