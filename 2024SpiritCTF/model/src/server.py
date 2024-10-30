import torch
import torch.nn as nn
import os
import time
import base64, io


class YuanSheNN(nn.Module):
    def __init__(self):
        super(YuanSheNN, self).__init__()
        self.fc1 = nn.Linear(256 * 256, 128)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(128, 1)

    def forward(self, x):
        x = x.view(x.size(0), -1)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x


for i in range(10):
    input_image = torch.randn(1, 1, 256, 256)
    target_output = torch.rand(1, 1) * 114514
    torch.save(input_image, "input")
    torch.save(target_output, "output")

    print(base64.b64encode(open("input", "rb").read()))
    print(base64.b64encode(open("output", "rb").read()))

    model = YuanSheNN()
    start_time = time.time()
    model.load_state_dict(
        torch.load(io.BytesIO(base64.b64decode(input("input base64:\n> "))))
    )
    # fc1_bias = torch.load(io.BytesIO(base64.b64decode(input("fc1 base64:\n> "))))
    # fc2_bias = torch.load(io.BytesIO(base64.b64decode(input("base64:\n> "))))
    # with torch.no_grad():
        # model.fc1.bias.copy_(fc1_bias)
        # model.fc2.bias.copy_(fc2_bias)
    if time.time() - start_time > 60:
        print("timeout")
        exit()
    output = model(input_image)
    if torch.abs(target_output - output) > 0.01:
        print("wrong")
        exit()
print("success")
print(open("/flag").read())