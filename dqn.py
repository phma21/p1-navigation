from collections import deque

import matplotlib.pyplot as plt
import numpy as np
import torch

from banana_env import BananaEnvWrapper
from dqn_agent import Agent

env = BananaEnvWrapper()

agent = Agent(state_size=env.state_size, action_size=env.action_space, seed=0)


# watch an untrained agent
def watch_untrained():
    state = env.reset()
    for j in range(200):
        action = agent.act(state)
        # env.render()
        state, reward, done = env.step(action)
        if done:
            break

    # env.close()
    env.reset()


def dqn(n_episodes=1000, max_t=1000, eps_start=1.0, eps_end=0.01, eps_decay=0.995):
    """Deep Q-Learning.

    Params
    ======
        n_episodes (int): maximum number of training episodes
        max_t (int): maximum number of timesteps per episode
        eps_start (float): starting value of epsilon, for epsilon-greedy action selection
        eps_end (float): minimum value of epsilon
        eps_decay (float): multiplicative factor (per episode) for decreasing epsilon
    """
    scores = []  # list containing scores from each episode
    scores_window = deque(maxlen=100)  # last 100 scores
    eps = eps_start  # initialize epsilon
    for i_episode in range(1, n_episodes + 1):
        state = env.reset()
        score = 0
        for t in range(max_t):
            action = agent.act(state, eps)
            next_state, reward, done = env.step(action)
            agent.step(state, action, reward, next_state, done)
            state = next_state
            score += reward
            if done:
                break
        scores_window.append(score)  # save most recent score
        scores.append(score)  # save most recent score
        eps = max(eps_end, eps_decay * eps)  # decrease epsilon
        print('\rEpisode {}\tAverage Score: {:.2f}\tEpsilon: {:.2f}'.format(i_episode, np.mean(scores_window), eps), end="")
        if i_episode % 100 == 0:
            print('\rEpisode {}\tAverage Score: {:.2f}'.format(i_episode, np.mean(scores_window)))
        # if np.mean(scores_window) >= 13.0:
        #     print('\nEnvironment solved in {:d} episodes!\tAverage Score: {:.2f}'.format(i_episode - 100,
        #                                                                                  np.mean(scores_window)))
        #     torch.save(agent.qnetwork_local.state_dict(), 'checkpoint.pth')
        #     break

    torch.save(agent.qnetwork_local.state_dict(), 'checkpoint.pth')
    return scores


def plot(scores):
    # plot the scores
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.plot(np.arange(len(scores)), scores)
    plt.ylabel('Score')
    plt.xlabel('Episode #')
    # plt.show()
    plt.savefig("eval_plot")

    scores_as_np = np.array(scores)
    print("Mean reward: ", np.mean(scores_as_np))


def train():
    scores = dqn()

    plot(scores)


def eval():

    # load the weights from file
    agent.qnetwork_local.load_state_dict(torch.load('checkpoint.pth'))
    # env.eval()

    scores = []
    for i in range(100):
        state = env.reset()
        scores.append(0)
        for j in range(1000):
            action = agent.act(state)
            # env.render()
            state, reward, done = env.step(action)
            scores[-1] += reward
            if done:
                break

    plot(scores)
    env.close()


if __name__ == '__main__':
    # train()
    eval()
