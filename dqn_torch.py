import gym
import numpy as np
import random
import torch 
import matplotlib.pyplot as plt
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from collections import namedtuple
import random
from torch.autograd import Variable
import torch.utils.data as utils_data
import sklearn.datasets as datasets
import network
import sys


Transition = namedtuple('Student',('state','action','next_state','reward')) 
BATCH_SIZE = 32



class ReplayMemory(object):
    
    def __init__(self,capacity):
        self.capacity = capacity
        self.memory = []
        self.position=0
    
    def push(self,*args):
        if len(self.memory) < self.capacity:
            self.memory.append(None)
        self.memory[self.position] = Transition(*args)
        self.position = (self.position +1)%self.capacity
    
    def sample(self,batch_size):
        return random.sample(self.memory,batch_size)
    
    def __len__(self):
        return len(self.memory)



class DQN:
    def __init__(self,layers):
        self.policy_net=network.Network(layers) # policy network
        self.memory = ReplayMemory(1000)
        self.optimizer = optim.RMSprop(self.policy_net.parameters())
        self.state_dimention = layers[0]
        self.n_action = layers[-1]
        self.nlayers = layers
        self.gamma = 0.95
        
    def select_action(self,state,eps=0.01):
        sample=random.random()
        state
        if sample<eps:
            return random.choice(range(self.n_action))
        else:
            return torch.max(self.policy_net(state),0)[1].tolist()
    
    def learn_model(self):
        if len(self.memory)<BATCH_SIZE:
            return
        transitions = self.memory.sample(BATCH_SIZE)

        batch = Transition(*zip(*transitions))
        state_batch = torch.tensor(batch.state)
        nextState_batch = torch.tensor(batch.next_state)
        reward_batch = torch.tensor(batch.reward)
        action_batch = torch.tensor(batch.action)
        
        state_action_values = self.policy_net(state_batch.float())
        
        next_state_value = self.policy_net(nextState_batch.float()).max(1)[0].detach()
        
        expected_rewards=next_state_value*self.gamma+reward_batch.float()
        
        target_action_values= state_action_values.clone()
        
        r_idx=torch.arange(target_action_values.size(0)).long()
        
        target_action_values[r_idx,action_batch] = expected_rewards
        
        loss = F.smooth_l1_loss(state_action_values,target_action_values)
        
        self.optimizer.zero_grad()
        
        loss.backward()
        
        for param in self.policy_net.parameters():#Gradient cliping to 
            param.grad.data.clamp_(-1,1)
            
        self.optimizer.step()
        
    def remember(self,state,action,next_state,reward):
        self.memory.push(state,action,next_state,reward)



class DDQN:
    def __init__(self,layers):
        self.policy_net=network.Network(layers) # policy network
        self.target_net=network.Network(layers) # target network 
        self.memory = ReplayMemory(1000)
        self.optimizer = optim.RMSprop(self.policy_net.parameters())
        self.state_dimention = layers[0]
        self.n_action = layers[-1]
        self.nlayers = layers
        self.gamma = 0.95
        
    
    def update_target_model(self):
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()
    
    def select_action(self,state,eps=0.01):
        sample=random.random()
        
        if sample<eps:
            return random.choice(range(self.n_action))
        else:
            return torch.max(self.policy_net(state),0)[1].tolist()
    
    def learn_model(self):
        if len(self.memory)<BATCH_SIZE:
            return
        transitions = self.memory.sample(BATCH_SIZE)
        batch = Transition(*zip(*transitions))


        state_batch = torch.tensor(batch.state)
        nextState_batch = torch.tensor(batch.next_state)
        reward_batch = torch.tensor(batch.reward)
        action_batch = torch.tensor(batch.action)
        
        state_action_values = self.policy_net(state_batch.float())
        
        next_state_value = self.target_net(nextState_batch.float()).max(1)[0].detach()
        
        expected_rewards=next_state_value*self.gamma+reward_batch.float()
        
        target_action_values= state_action_values.clone()
        
        r_idx=torch.arange(target_action_values.size(0)).long()
        
        target_action_values[r_idx,action_batch] = expected_rewards
        
        loss = F.smooth_l1_loss(state_action_values,target_action_values)
        
        self.optimizer.zero_grad()
        
        loss.backward()
        
        for param in self.policy_net.parameters():
            param.grad.data.clamp_(-1,1)
            
        self.optimizer.step()
    
    def remember(self,state,action,next_state,reward):
        self.memory.push(state,action,next_state,reward)


def plot_running_avg(totalrewards):
    N = len(totalrewards)
    running_avg = np.empty(N)
    for t in range(N):
        running_avg[t] = totalrewards[max(0, t-100):(t+1)].mean()
    plt.plot(running_avg)
    plt.title("Running Average")
    plt.show()


if __name__ == '__main__':
    import matplotlib
    import matplotlib.pyplot as plt
    from gym import wrappers
    from datetime import datetime
    import math

    import os
    env = gym.make('CartPole-v0').env
    is_ipython = 'inline' in matplotlib.get_backend()

    if is_ipython:
        from IPython import display
    plt.ion()
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.n
    agent=DDQN([state_size,10,10,action_size])
    done = False
    BATCH_SIZE = 128
    argv='monitor'
    filename="test"
    EPS_START = 0.9
    EPS_END = 0.05
    EPS_DECAY = 200
    done=False
    t=0
    num_episodes = 1000
    rewards=[]
    if 'monitor' in sys.argv:
        #filename = os.path.basename(__file__).split('.')[0]
        monitor_dir = './' + filename + '_' + str(datetime.now())
        env = wrappers.Monitor(env, monitor_dir)
    for e in range(num_episodes):
        state =env.reset()
        done=False
        t=0
        totalreward = 0
        while not done and t<10000:
            eps_threshold = EPS_END + (EPS_START - EPS_END)* math.exp(-1. * t / EPS_DECAY)
            action = agent.select_action(torch.from_numpy(state).float())
            next_state,reward,done,_ = env.step(action)
            
            reward = reward if not done else -10
            
            agent.remember(state.tolist(),action,next_state.tolist(),reward)
            state = next_state
            agent.learn_model()
            if done :
                agent.update_target_model()
                if t<199:
                    reward =-200
                #print("Time: {} , Reward: {}".format(t,totalreward))
            totalreward += reward
            t += 1
        rewards.append(totalreward)
    
    plt.plot(rewards)
    plt.title("Rewards")
    plt.show()

    plot_running_avg(np.array(rewards))

    
        
    env.close()