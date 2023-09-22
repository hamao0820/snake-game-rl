import random
from collections import deque
from typing import Tuple

import numpy as np


class ReplayBuffer:
    def __init__(self, buffer_size: int, batch_size: int) -> None:
        self.buffer: deque[Tuple[np.ndarray, int, float, np.ndarray, bool]] = deque(maxlen=buffer_size)

        self.batch_size = batch_size

    def add(self, state: np.ndarray, action: int, reward: float, next_state, done: bool) -> None:
        data = (state, action, reward, next_state, done)

        self.buffer.append(data)

    def __len__(self) -> int:
        return len(self.buffer)

    def get_batch(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        data = random.sample(self.buffer, self.batch_size)

        state = np.stack([x[0] for x in data], axis=0, dtype=np.float32)
        action = np.array([x[1] for x in data], dtype=np.int32)
        reward = np.array([x[2] for x in data], dtype=np.float32)
        next_state = np.stack([x[3] for x in data], axis=0, dtype=np.float32)
        done = np.array([x[4] for x in data], dtype=np.int32)
        return state, action, reward, next_state, done
