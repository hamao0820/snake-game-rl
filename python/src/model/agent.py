import copy

import numpy as np
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from QNet import QNet
from replay_buffer import ReplayBuffer


class DQNAgent:
    def __init__(self):
        self.gamma = 0.98
        self.lr = 0.0005
        self.epsilon = 0.1
        self.buffer_size = 10000
        self.batch_size = 32
        self.action_size = 2

        self.replay_buffer = ReplayBuffer(self.buffer_size, self.batch_size)
        self.qnet = QNet(self.action_size)
        self.qnet_target = QNet(self.action_size)
        self.optimizer = optim.Adam(self.qnet.parameters(), lr=self.lr)

    # 同期メソッド
    def sync_qnet(self):
        # Q関数NNとターゲットNNを同期
        self.qnet_target = copy.deepcopy(self.qnet)

    # 行動メソッドの定義
    def get_action(self, state):
        # ε-greedy法により行動を決定:式(6.11)
        if np.random.rand() < self.epsilon:
            # ランダムに行動を出力
            return np.random.choice(self.action_size)
        else:
            # 2次元配列に変換
            state = state[np.newaxis, :]

            # 現在の状態における行動価値(Q関数NNの順伝播)を計算
            qs = self.qnet(state)

            # 行動価値が最大の行動を出力
            return qs.data.argmax()

    # 更新メソッドの定義
    def update(self, state, action, reward, next_state, done):
        # サンプルデータを保存
        self.replay_buffer.add(state, action, reward, next_state, done)

        # サンプルデータが足りない場合は更新しない
        if len(self.replay_buffer) < self.batch_size:
            return None

        # ミニバッチデータを取得
        state, action, reward, next_state, done = self.replay_buffer.get_batch()

        # サンプルごとに現在の状態・行動の行動価値(Q関数NNの順伝播)を計算
        qs = self.qnet(state)  # 全ての行動
        q = qs[np.arange(self.batch_size), action]  # 各行動

        # サンプルごとに次の状態の行動価値(ターゲットNNの順伝播)の最大値を計算
        next_qs = self.qnet_target(next_state)  # 全ての行動
        next_q = next_qs.max(axis=1)  # 最大値の行動

        # 勾配の計算から除外
        next_q.unchain()

        # ターゲット(正解ラベル)を計算
        target = reward + (1 - done) * self.gamma * next_q

        # 損失関数(損失レイヤの順伝播)を計算
        loss = nn.mean_squared_error(q, target)

        # 勾配を初期化
        self.qnet.cleargrads()

        # パラメータの勾配(逆伝播)を計算
        loss.backward()

        # 勾配降下法によりQ関数NNのパラメータを更新
        self.optimizer.update()

        # 損失を出力
        return loss.data
