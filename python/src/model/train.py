from typing import List

import numpy as np
from agent import DQNAgent
from environment import SnakeGameEnv
import torch

device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

env = SnakeGameEnv()
agent = DQNAgent(device=device)

episodes = 500

sync_interval = 10

trace_loss: List[float] = []
trace_reward: List[float] = []

for episode in range(episodes):
    state, info = env.reset()
    done = False

    t = 0

    total_loss = 0.0
    total_reward = 0.0

    while not done:
        t += 1

        action = agent.get_action(state)

        next_state, reward, done, truncated, info = env.step(action)

        loss = agent.update(state, action, reward, next_state, done)

        state = next_state

        if not len(agent.replay_buffer) < agent.batch_size:
            total_loss += loss
        total_reward += reward

    if episode % sync_interval == 0:
        agent.sync_qnet()

    trace_loss.append(total_loss / t)
    trace_reward.append(total_reward)

    print(
        "episode "
        + str(episode + 1)
        + ", T="
        + str(t)
        + ", average loss="
        + str(np.round(total_loss / t, 5))
        + ", total reward="
        + str(total_reward)
    )
    if (episode + 1) % 5 == 0:
        agent.save(f"{episode + 1}_dqn_weight")
        env.render(f"img/{episode + 1}_snake-game.gif")

agent.save()

env.close()
