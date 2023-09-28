from itertools import count

import cv2
import matplotlib.pyplot as plt
import numpy as np
import torch
from agent import DQNAgent
from environment import SnakeGameEnv
from tqdm import tqdm

num_episodes = 5000000  # 学習させるエピソード数

n_frame = 6
resize_image = 84
reward_clipping = True  # 報酬のクリッピング

num_episode_plot = torch.tensor([10])  # 何エピソードで学習の進捗を確認するか
num_episode_save = 5  # 何エピソードでモデルを保存するか

device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")


def to_resize_gray(image: np.ndarray, resize: int) -> torch.Tensor:
    m_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    m_image = cv2.resize(src=m_image, dsize=(resize, resize)) / 255.0
    t_image = torch.tensor(m_image, dtype=torch.float32).unsqueeze(0).unsqueeze(0)
    return t_image


env = SnakeGameEnv()
n_actions = env.action_space.n
agent = DQNAgent(n_frame=n_frame, device=device, state_dict_path="model_weights/11/snake-game_policy.pth")

terminated = True
frame1 = True
total_steps = 0
count_update = 0
steps_done = 0
reward_all = -num_episode_plot * 0.75 + 1
reward_durations = []

for i_episode in tqdm(range(num_episodes)):
    reward_frame = torch.tensor([0], dtype=torch.float32)
    if terminated == True:
        state_frame = torch.zeros((1, n_frame, resize_image, resize_image), dtype=torch.float32)
        next_state_frame = torch.zeros((1, n_frame, resize_image, resize_image), dtype=torch.float32)
        state, info = env.reset()
        t_state = to_resize_gray(state, resize_image)
        state_frame[:, 0, :, :] = t_state
        next_state_frame[:, 0, :, :] = t_state

    for t in count():
        total_steps += 1
        action, eps_threshold = agent.e_greedy_select_action(state_frame, steps_done)
        steps_done += 1
        observation, reward, terminated, truncated, info = env.step(action.item())

        done = terminated or truncated

        t_reward = torch.tensor([reward])
        reward_all += t_reward
        if reward_clipping:  # 報酬のクリッピング
            t_reward = torch.clamp(input=t_reward, min=-1, max=1)

        next_state = to_resize_gray(observation, resize_image)
        # rollして一番古いフレームを新しいフレームで上書きする
        next_state_frame = torch.roll(input=next_state_frame, shifts=1, dims=1)
        next_state_frame[:, 0, :, :] = next_state

        if frame1 == True:
            state_frame1 = state_frame
            action_frame1 = action
            next_state_frame1 = next_state_frame
            if done:
                next_state_frame1 = torch.zeros((1, n_frame, resize_image, resize_image), dtype=torch.float32)
            frame1 = False

        reward_frame += t_reward

        if (total_steps % n_frame == 0) or done:
            agent.push_memory(state_frame1, action_frame1, next_state_frame1, reward_frame)
            frame1 = True
            reward_frame = torch.tensor([0], dtype=torch.float32)

            count_update += 1
            if count_update % 4 == 0:
                if count_update > agent.SIZE_REPLAY_MEMORY:
                    agent.update()
            if count_update % 400 == 0:
                agent.sync_target()

        state_frame = next_state_frame
        if done:
            break
    if i_episode % num_episode_plot == 0:
        reward_durations.append(reward_all / num_episode_plot)
        plt.figure(1)
        plt.clf()
        plt.xlabel("Episode")
        plt.ylabel("Reward")
        plt.plot(
            np.arange(0, (i_episode / num_episode_plot + 1) * num_episode_plot, num_episode_plot),
            torch.tensor(reward_durations, dtype=torch.float).numpy(),
        )
        plt.savefig(f"progress/reward_duration.png")
        plt.clf()

        if (i_episode % num_episode_save) == 0:
            agent.save()
            env.render()

agent.save()
env.close()
