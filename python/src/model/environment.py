import io
import sys
from typing import List, Literal, Tuple, TypeAlias

import cv2
import numpy as np
import PIL.Image as Image

sys.path.append("./src/websocketClient")
from websocket_client import Action, WebsocketClient

Action_Space: TypeAlias = Tuple[Literal[0], Literal[1], Literal[2]]


class ActionSpace:
    def __init__(self) -> None:
        self.__action_space: Action_Space = (0, 1, 2)
        return

    @property
    def action_space(self) -> Action_Space:
        return self.__action_space

    @property
    def n(self) -> int:
        return len(self.__action_space)


class SnakeGameEnv:
    def __init__(self) -> None:
        self.__client = WebsocketClient()
        self.__action_space = ActionSpace()
        self.__client.connect()
        self.__frames: List[np.ndarray] = []
        return

    def reset(self) -> Tuple[np.ndarray, dict]:
        state, info = self.__client.reset()
        frame_image = cv2.imdecode(np.frombuffer(io.BytesIO(bytes(state["data"])).read(), np.uint8), cv2.IMREAD_COLOR)
        frame_array = np.array(frame_image)
        self.__frames = [frame_array]
        return frame_array, info

    def step(self, action: Action) -> Tuple[np.ndarray, float, bool, bool, dict]:
        observation, reward, terminated, truncated, info = self.__client.step(action)
        frame_image = cv2.imdecode(
            np.frombuffer(io.BytesIO(bytes(observation["data"])).read(), np.uint8), cv2.IMREAD_COLOR
        )
        frame_array = np.array(frame_image)
        self.__frames.append(frame_array)
        return frame_array, reward, terminated, truncated, info

    def close(self) -> None:
        self.__client.close()

    def render(self, fname: str = "snake-game") -> None:
        images = [Image.fromarray(frame) for frame in self.__frames]
        images[0].save(
            f"img/{fname}.gif",
            save_all=True,
            append_images=images[1:],
            duration=100,
            loop=0,
        )

    @property
    def action_space(self) -> ActionSpace:
        return self.__action_space
