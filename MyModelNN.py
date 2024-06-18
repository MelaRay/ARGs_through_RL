import torch

#Réseau de neurones 'classique' prenant en entrée un vecteur
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

#Réseau de neurones 'classique' prenant en entrée une matrice 
class MyModel2(torch.nn.Module):

    def __init__(self):
        super(MyModel2, self).__init__()
        self.layer1 = torch.nn.Flatten(0,1)
        self.linear1 = torch.nn.Linear(160, 80)
        self.activation = torch.nn.ReLU()
        self.linear2 = torch.nn.Linear(80, 1)
        #self.activation2 = torch.nn.ReLU()
        #self.linear3 = torch.nn.Linear(40, 1)
        #self.activation3 = torch.nn.Sigmoid()
        #self.linear4 = torch.nn.Linear(20, 1)


    def forward(self, x):
        x = self.layer1(x)
        x = self.linear1(x)
        x = self.activation(x)
        x = self.linear2(x)
        #x = self.activation2(x)
        #x = self.linear3(x)
        #x = self.activation3(x)
        #x = self.linear4(x)
        return x
    
#Réseau de neurones de convolution prenant en entrée une matrice     
class MyModel3(torch.nn.Module):

    def __init__(self):
        super(MyModel3, self).__init__()
        self.conv = torch.nn.Conv2d(1, 10, kernel_size = (1,3))
        self.act = torch.nn.LeakyReLU()
        self.conv2 = torch.nn.Conv2d(10, 50,kernel_size = (1,8))
        self.act2 = torch.nn.Tanh()
        self.conv3 = torch.nn.Conv2d(50, 250, kernel_size = (6,1))
        self.act3 = torch.nn.Tanh()
        self.layer1 = torch.nn.Flatten(0,2)
        self.linear1 = torch.nn.Linear(250, 125)
        self.activation = torch.nn.LeakyReLU()
        self.linear2 = torch.nn.Linear(125, 1)
        #self.activation2 = torch.nn.Tanh()
        #self.linear3 = torch.nn.Linear(60, 1)
        #self.activation3 = torch.nn.Sigmoid()
        #self.linear4 = torch.nn.Linear(20, 1)


    def forward(self, x):
        x = self.conv(x)
        x = self.act(x)
        x = self.conv2(x)
        x = self.act2(x)
        x = self.conv3(x)
        x = self.act3(x)
        x = self.layer1(x)
        x = self.linear1(x)
        x = self.activation(x)
        x = self.linear2(x)
        #x = self.activation2(x)
        #x = self.linear3(x)
        #x = self.activation3(x)
        #x = self.linear4(x)
        return x