import dqn_torch
import torch

# epsilon statergies 

class DQN_agent(object):
    def __init__(self,
        layers,replay_size=1000,
        batch_size=128,eps=0.1,gamma=0.95):

        self.DDQN = dqn_torch.DDQN(layers,replay_size,batch_size)
        self.eps = eps
        self.oldState =None
        self.oldAction=None
        self.t=0
        self.decayTill = 0
        self.eps_decay = 0.99

    def learn(self,state,reward):
        if self.oldState==None: return
        self.DDQN.remember(self.oldState,self.oldAction,state,reward)
        self.DDQN.learn_model()

        if self.t%100 ==0:
            self.DDQN.update_target_model()
  

    def do(self,state):
        self.oldState = state
        action=self.DDQN.select_action(torch.tensor(state).float(),self.eps)

        self.t += 1
        if self.t %100 == 0 and self.eps > self.decayTill:
            self.eps *= self.eps_decay
            #self.t= 0 

        self.oldAction=action
        return action

    




