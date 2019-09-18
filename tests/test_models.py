from collections import OrderedDict
from itertools import product
import torch
from torchvision import models
import unittest

from models.mobilenet import mobilenet_v2
from models.squeezenet import squeezenet1_0, squeezenet1_1
from models.resnet import resnet18, resnet34, resnet50, resnet101, resnet152, resnext50_32x4d, resnext101_32x8d

models_dict = {
    'mobilenet_v2' : mobilenet_v2,
    'squeezenet1_0' : squeezenet1_0,
    'squeezenet1_1' : squeezenet1_1,
    'resnet18' : resnet18,
    'resnet34' : resnet34,
    'resnet50' : resnet50,
    'resnet101' : resnet101,
    'resnet152' : resnet152,
    'resnext50_32x4d' : resnext50_32x4d,
    'resnext101_32x8d' : resnext101_32x8d,
}

class Tester(unittest.TestCase):

    def _test_classification_model(self, name, input_shape):
        # passing num_class equal to a number other than 1000 helps in making the test
        # more enforcing in nature
        model = models_dict[name](num_classes=50)
        model.eval()
        x = torch.rand(input_shape)
        out = model(x)
        self.assertEqual(out.shape[-1], 50)


    def _test_equal(self, name, input_shape):
        model1 = models_dict[name](pretrained=True, num_classes=50)
        model1.eval()
        x = torch.rand(input_shape)
        out1 = model1(x)
        model = models.__dict__[name](num_classes=50)
        model.load_state_dict(model1.state_dict())
        model.eval()
        out2 = model(x)
        self.assertListEqual(list(out1.detach().numpy().round(6).flatten()), list(out2.detach().numpy().round(6).flatten()))



for model_name in models_dict.keys():
    # for-loop bodies don't define scopes, so we have to save the variables
    # we want to close over in some way
    def do_test(self, model_name=model_name):
        input_shape = (1, 3, 224, 224)
        self._test_classification_model(model_name, input_shape)
        self._test_equal(model_name, input_shape)

    setattr(Tester, "test_" + model_name, do_test)


if __name__ == '__main__':
    unittest.main()