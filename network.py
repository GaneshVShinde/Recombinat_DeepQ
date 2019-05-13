import torch


class Single_net(torch.nn.Module):
    def __init__(self, n_feature, n_hidden, n_output):
        super(Single_net, self).__init__()
        self.hidden = torch.nn.Linear(n_feature, n_hidden)   # hidden layer
        self.predict = torch.nn.Linear(n_hidden, n_output)   # output layer

    def forward(self, x):
        tanh = torch.nn.ReLU()
        x = tanh(self.hidden(x))      # activation function for hidden layer
        x = self.predict(x)             # linear output
        return x


class Network(torch.nn.Module):
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