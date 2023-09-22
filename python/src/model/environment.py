import io
import sys
from typing import Literal, Tuple, TypeAlias

import numpy as np
import PIL.Image as Image

sys.path.append("./src/websocketClient")
from websocket_client import Action, WebsocketClient

Action_Space: TypeAlias = Tuple[Literal[0], Literal[1], Literal[2]]


class SnakeGameEnv:
    def __init__(self) -> None:
        self.__client = WebsocketClient()
        self.__action_space: Action_Space = (0, 1, 2)
        self.__client.connect()
        return

    def reset(self) -> Tuple[np.ndarray, dict]:
        state, info = self.__client.reset()
        image_arr = np.array(Image.open(io.BytesIO(bytes(state["data"]))).convert("RGB"))
        return image_arr, info

    def step(self, action: Action) -> Tuple[np.ndarray, float, bool, bool, dict]:
        observation, reward, terminated, truncated, info = self.__client.step(action)
        image_arr = np.array(Image.open(io.BytesIO(bytes(observation["data"]))).convert("RGB"))
        return image_arr, reward, terminated, truncated, info

    def close(self) -> None:
        self.__client.close()

    @property
    def action_space(self) -> Action_Space:
        return self.__action_space
