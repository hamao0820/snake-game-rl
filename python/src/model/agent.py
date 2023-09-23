import copy

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from QNet import QNet
from replay_buffer import ReplayBuffer


class DQNAgent:
    def __init__(self):
        self.gamma = 0.98
        self.lr = 0.0005
        self.epsilon = 0.3
        self.buffer_size = 300
        self.batch_size = 32
        self.action_size = 3

        self.replay_buffer = ReplayBuffer(self.buffer_size, self.batch_size)
        self.qnet = QNet(self.action_size)
        self.qnet_target = QNet(self.action_size)
        self.optimizer = optim.Adam(self.qnet.parameters(), lr=self.lr)

    def sync_qnet(self) -> None:
        self.qnet_target = copy.deepcopy(self.qnet)

    def get_action(self, state: np.ndarray) -> int:
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.action_size)
        else:
            state = state[np.newaxis, :]

            qs = self.qnet(torch.from_numpy(state))

            return qs.data.argmax().item()

    def update(self, state: np.ndarray, action: int, reward: float, next_state: np.ndarray, done: bool) -> float:
        self.replay_buffer.add(state, action, reward, next_state, done)

        if len(self.replay_buffer) < self.batch_size:
            return 0

        state, action, reward, next_state, done = self.replay_buffer.get_batch()

        qs = self.qnet(torch.from_numpy(state))
        q = qs[np.arange(self.batch_size), action]

        next_qs = self.qnet_target(torch.from_numpy(next_state))
        next_q = torch.max(next_qs, dim=1, keepdim=True).values.detach().squeeze()

        target = torch.tensor(reward) + (1 - torch.tensor(done)) * self.gamma * next_q

        loss = F.mse_loss(q, target)

        self.qnet.zero_grad()

        loss.backward()

        self.optimizer.step()

        return loss.data.item()

    def save(self, name: str = "dqn_weight") -> None:
        torch.save(self.qnet.state_dict(), "model_weights/" + name + ".pth")
        torch.save(self.qnet_target.state_dict(), "model_weights/" + name + "_target" + ".pth")
