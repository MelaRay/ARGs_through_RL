import torch

#Module to create model to approximate value function
#Neural network to approximate value function
class MyModel(torch.nn.Module):

    def __init__(self):
        super(MyModel, self).__init__()

        self.linear1 = torch.nn.Linear(216, 108)
        torch.nn.init.normal_(self.linear1.weight, mean=0, std=0.01)
        torch.nn.init.normal_(self.linear1.bias, mean=0, std=0.01)
        self.activation = torch.nn.ReLU()
        self.linear2 = torch.nn.Linear(108, 1)
        torch.nn.init.normal_(self.linear2.weight, mean=0, std=0.01)
        torch.nn.init.normal_(self.linear2.bias, mean=0, std=0.01)
        self.activation2 = torch.nn.ReLU()


    def forward(self, x):
        x = self.linear1(x)
        x = self.activation(x)
        x = self.linear2(x)
        x = torch.multiply(self.activation2(x), -1)
        return x
