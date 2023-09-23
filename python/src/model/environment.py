import io
import sys
from typing import List, Literal, Tuple, TypeAlias

import numpy as np
import PIL.Image as Image
import cv2

sys.path.append("./src/websocketClient")
from websocket_client import Action, WebsocketClient

Action_Space: TypeAlias = Tuple[Literal[0], Literal[1], Literal[2]]


class SnakeGameEnv:
    def __init__(self) -> None:
        self.__client = WebsocketClient()
        self.__action_space: Action_Space = (0, 1, 2)
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
        frame_image = Image.open(io.BytesIO(bytes(observation["data"]))).convert("RGB")
        self.__frames.append(np.array(frame_image))
        state = np.transpose(np.expand_dims(np.array(frame_image.resize((84, 84)).convert("L")), axis=2), (2, 0, 1))
        return state, reward, terminated, truncated, info

    def close(self) -> None:
        self.__client.close()

    def render(self, path: str = "img/snake-game.gif") -> None:
        images = [Image.fromarray(frame) for frame in self.__frames]
        images[0].save(
            path,
            save_all=True,
            append_images=images[1:],
            duration=100,
            loop=0,
        )

    @property
    def action_space(self) -> Action_Space:
        return self.__action_space
