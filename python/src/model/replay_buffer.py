import random
from collections import deque, namedtuple
from typing import List

Transition = namedtuple("Transition", ("state", "action", "next_state", "reward"))


class ReplayMemory(object):
    def __init__(self, capacity: int):
        self.memory: deque[Transition] = deque(maxlen=capacity)

    def push(self, *args) -> None:
        self.memory.append(Transition(*args))

    def sample(self, batch_size) -> List[Transition]:  # batch_size分ランダムにメモリから抽出
        return random.sample(self.memory, batch_size)

    def __len__(self) -> int:
        return len(self.memory)
