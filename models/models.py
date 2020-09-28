import torch
import torch.nn as nn

rdc_text_dim = 1000
z_dim = 100
h_dim = 4086


class _param:
    def __init__(self):
        self.rdc_text_dim = rdc_text_dim
        self.z_dim = z_dim
        self.h_dim = h_dim


# reduce to dim of text first
class _netG(nn.Module):
    def __init__(self, text_dim=11083, X_dim=3584):
        super(_netG, self).__init__()
        self.rdc_text = nn.Linear(text_dim, rdc_text_dim)
        self.main = nn.Sequential(nn.Linear(z_dim + rdc_text_dim, h_dim),
                                  nn.LeakyReLU(),
                                  nn.Linear(h_dim, X_dim),
                                  nn.Tanh())

    def forward(self, z, c):
        rdc_text = self.rdc_text(c)
        input = torch.cat([z, rdc_text], 1)
        output = self.main(input)
        return output


class _netD(nn.Module):
    def __init__(self, y_dim=150, X_dim=3584):
        super(_netD, self).__init__()
        # Discriminator net layer one
        self.D_shared = nn.Sequential(nn.Linear(X_dim, h_dim),
                                      nn.ReLU())
        # Discriminator net branch one: For Gan_loss
        self.D_gan = nn.Linear(h_dim, 1)
        # Discriminator net branch two: For aux cls loss
        self.D_aux = nn.Linear(h_dim, y_dim)

    def forward(self, input):
        h = self.D_shared(input)
        # print('input is', input.shape)
        return self.D_gan(h), self.D_aux(h)


# semantic guided categorizer
class _netGSGC(nn.Module):
    def __init__(self, text_dim=11083, X_dim=3584):
        super(_netGSGC, self).__init__()
        self.rdc_text = nn.Linear(text_dim, rdc_text_dim)
        self.main = nn.Sequential(nn.Linear(z_dim + rdc_text_dim, h_dim),
                                  nn.LeakyReLU(),
                                  nn.Linear(h_dim, X_dim),
                                  nn.Tanh())

    def forward(self, z, c):
        rdc_text = self.rdc_text(c)
        input = torch.cat([z, rdc_text], 1)
        output = self.main(input)
        return rdc_text, output


class _netDSGC(nn.Module):
    def __init__(self, y_dim=150, X_dim=3584, rdc_text_dim = 1000):
        super(_netDSGC, self).__init__()
        # Discriminator net layer one
        self.D_shared = nn.Sequential(nn.Linear(X_dim, h_dim),
                                      nn.ReLU())
        # Discriminator net branch one: For Gan_loss
        self.D_gan = nn.Linear(h_dim, 1)
        # # Discriminator net branch two: For aux cls loss
        # self.D_aux = nn.Linear(h_dim, y_dim)
        # semantic guided categorizer
        self.D_SGC = nn.Linear(h_dim, rdc_text_dim)

    def forward(self, input):
        h = self.D_shared(input)
        # print(h.shape, input.shape)
        # print('input is', input.shape)
        # return self.D_gan(h), self.D_aux(h)
        return self.D_gan(h), self.D_SGC(h)

# semantic guided categorizer
class _netGSGCCLS(nn.Module):
    def __init__(self, text_dim=11083, X_dim=3584):
        super(_netGSGCCLS, self).__init__()
        self.rdc_text = nn.Linear(text_dim, rdc_text_dim)
        self.main = nn.Sequential(nn.Linear(z_dim + rdc_text_dim, h_dim),
                                  nn.LeakyReLU(),
                                  nn.Linear(h_dim, X_dim),
                                  nn.Tanh())

    def forward(self, z, c):
        rdc_text = self.rdc_text(c)
        input = torch.cat([z, rdc_text], 1)
        output = self.main(input)
        return rdc_text, output


# semantic guided matrix with classifications
class _netDSGCCLS(nn.Module):
    def __init__(self, y_dim=150, X_dim=3584, rdc_text_dim = 1000):
        super(_netDSGCCLS, self).__init__()
        # Discriminator net layer one
        self.D_shared = nn.Sequential(nn.Linear(X_dim, h_dim),
                                      nn.ReLU())
        # Discriminator net branch one: For Gan_loss
        self.D_gan = nn.Linear(h_dim, 1)
        # Discriminator net branch two: For aux cls loss
        self.D_aux = nn.Linear(h_dim, y_dim)
        # Discriminator net branch three: semantic guided categorizer
        self.D_SGC = nn.Linear(h_dim, rdc_text_dim)

    def forward(self, input):
        h = self.D_shared(input)
        # print(h.shape, input.shape)
        return self.D_gan(h), self.D_aux(h), self.D_SGC(h)

