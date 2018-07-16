import torch as t
import Blocks
from Blocks import RNN

def loss(logits, target):
    loss = None
    return loss

class ELMO(t.nn.Module):
    #TODO: complete elmo model
    def __init__(self, matrix, encoder='RNN'):
        super(ELMO, self).__init__()
        self.max_lenth = 40
        self.model = getattr(Blocks, encoder)()
        self.embedding = t.nn.Embedding(matrix.size()[0], matrix.size()[1])
        self.elmo_rnn = RNN()

    def forward(self, inputs):
        pass

    def get_loss_func(self):
        return loss

    def get_optimizer(self):
        return t.optim.Adam(self.parameters())
