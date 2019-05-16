import torch


class Single_net(torch.nn.Module): #regression network1
    def __init__(self, n_feature, n_hidden, n_output):
        super(Single_net, self).__init__()
        self.hidden = torch.nn.Linear(n_feature, n_hidden)   # hidden layer
        self.predict = torch.nn.Linear(n_hidden, n_output)   # output layer

    def forward(self, x):
        relu = torch.nn.ReLU()
        x = relu(self.hidden(x))      # activation function for hidden layer
        x = self.predict(x)             # linear output
        return x



class Network(torch.nn.Module): #regression network 2
    def __init__(self,layers):
        super(Network, self).__init__()
        self.nLayers= len(layers)
        self.layers = layers
        self.linear = torch.nn.ModuleList()
        for i in range(len(layers)-1):
            self.linear.append(torch.nn.Linear(layers[i],layers[i+1]))
        
    def forward(self,out):
        tanh = torch.nn.ReLU()
        for i in range(self.nLayers-2):
            out = self.linear[i](out)
            out = tanh(out)
        out = self.linear[-1](out)
        return out


class base_network(torch.nn.Module):
    def __init__(self,layers):
        super(base_network,self).__init__()
        self.nLayers = len(layers)
        self.layers = layers
        self.linear = torch.nn.ModuleList()
        self.tanh = torch.nn.Tanh()
        for i in range(self.nLayers-1):
            self.linear.append(torch.nn.Linear(layers[i],layers[i+1]))
    
    def forward(self,out):
        for i in range(self.nLayers-1):
            out=self.linear[i](out)
            out=self.tanh(out)
        return out

class internal_memory:
    def __init__(self,layers):
        self.memory = base_network(layers)
        self.optimizer= torch.optim.SGD(self.memory.parameters(),lr=0.001)
        self.loss = torch.nn.MSELoss()
        self.output =[0]

    def trainOne(self,input,target):
        prediction=self.memory(torch.tensor(input).float())
        self.optimizer.zero_grad()
        loss=self.loss(prediction,torch.tensor([target]).float())
        loss.backward()
        self.optimizer.step()

    def update(self,input):
        self.output=self.memory(torch.tensor(input).float()).tolist()
        return self.output[0]
        





def train(net,X,y,no_epochs,loss_func,optimizer):
    losses=[]
    for t in range(no_epochs):
        optimizer.zero_grad()   # clear gradients for next train
        prediction = net(X)     # input X and predict based on X
        loss = loss_func(prediction, y)
        loss.backward()         # backpropagation, compute gradients
        optimizer.step()        # apply gradients
        if t % 5 == 0:
            losses.append(loss.data.numpy())
    return(losses)


def test_network(net=None): # this code simply checks with only test data
    ## creating artificial data
    import sklearn.datasets as datasets
    import matplotlib.pyplot as plt
    X_,y_=datasets.make_regression(n_samples=1000,n_features=2,noise=0.1)
    X = torch.from_numpy(X_).float()
    y = torch.from_numpy(y_).float()
    y=y.view(1000,1)

    #net = Net(n_feature=2, n_hidden=10, n_output=1)     # define the network
    if net==None:
        net=Network([2,10,1])
    print(net)  # net architecture

    optimizer = torch.optim.Adam(net.parameters(), lr=0.01)
    loss_func = torch.nn.MSELoss()  # this is for regression mean squared loss
    
    loss_func2 = torch.nn.functional.smooth_l1_loss
    optimizer2 = torch.optim.RMSprop(net.parameters())

    losses=train(net,X,y,200,loss_func2,optimizer2)
    prediction=net(X)
    plt.plot(losses)
    plt.show()
    plt.figure()
    plt.scatter(range(len(y_)),y_,s=2,label="actual")
    plt.scatter(range(len(y_)),prediction.data.numpy(),s=2,label="predicted")
    plt.legend()
    plt.show()