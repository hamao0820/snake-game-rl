import asyncio
from typing import Generic, Literal, Tuple, TypeAlias, TypeVar

from websocketClient.websocket_client import Action, WebsocketClient

Action_Space: TypeAlias = Tuple[Literal[0], Literal[1], Literal[2]]
ObsType = TypeVar("ObsType")


class SnakeGameEnv(Generic[ObsType]):
    def __init__(self) -> None:
        self.client = WebsocketClient()
        asyncio.get_event_loop().run_until_complete(self.client.connect())
        self.__action_space: Action_Space = (0, 1, 2)
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
