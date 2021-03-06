import os
import sys
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

import chainer
import chainer.functions as F
from chainer import reporter

import ebnn.links as BL


class ConvNet(BL.CChainMixin, chainer.Chain):
    def __init__(self, n_filters, n_out):
        super(ConvNet, self).__init__()
        self.n_filters = n_filters
        self.n_out = n_out
        with self.init_scope():
            self.l1 = BL.ConvBNBST(n_filters, 3)
            self.l2 = BL.BinaryLinearBNSoftmax(n_out)

    def link_order(self):
        return [self.l1,  self.l2]

    def __call__(self, x, t, ret_param='loss'):
        h = self.l1(x)
        h = self.l2(h)

        # reports loss and accuracy (used during training)
        report = {
            'loss': F.softmax_cross_entropy(h, t),
            'acc': F.accuracy(h, t)
        }

        reporter.report(report, self)
        return report[ret_param]

    # Determines what is output each iteration during training
    # (shouldn't need to change this unless your network is complex)
    def report_params(self):
        return ['validation/main/acc']

    # A unique identifier of the model (used to save models)
    # I prefer this over random generated ids as its readable
    def param_names(self):
        # in this case, n_units and n_out define the model
        return 'ConvNet{}_{}'.format(self.n_filters, self.n_out)
