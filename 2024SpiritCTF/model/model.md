model

模型是一个简单的fc -> relu -> fc。

fc2(relu(fc1(x))) = fc2(relu(W1x +B1)) = W2 relu(W1x + B1) + B2。观察发现，输出值的relu(W1x + B1)  和 B2 都可以固定。所以输出的答案是能够固定的。

![Relu](/Users/libr/Desktop/出题/model/relu.jpg)

B1 设置为一个很大的数=> relu(W1x + B1) = 0

B2 设置为预期输出 => fc2(relu(fc1(x))) = B2 = output

另外就是 pwntools 的发送是有限制的。

可以直接使用 socket 进行交互。

```python
import torch
import torch.nn as nn
from pwn import *
from base64 import b64decode, b64encode
import io
context.log_level = "debug"
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


model = YuanSheNN()
import socket
r = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
r.connect(("202.198.27.90",40149))
# r = remote("127.0.0.1",1145)
for i in range(10):
    print(i)
    recv = b""
    while True:
        recved = r.recv(1024)
        print(recved)
        recv += recved
        if b"input base64:\n> " in recv:
            break
    recv = recv.split(b"\n")
    print(recv)
    input_image = torch.load(io.BytesIO(b64decode(eval(recv[0]))))
    target_output = torch.load(io.BytesIO(b64decode(eval(recv[1]))))
    with torch.no_grad():
        model.fc1.bias.copy_(torch.ones(128)*-1e10)
        model.fc2.bias.copy_(target_output.reshape(1))
    fc1 = io.BytesIO()
    fc2 = io.BytesIO()
    # torch.save(model.fc1.bias, fc1)
    torch.save(model.state_dict(), fc2)
    # r.sendlineafter(b"fc1 base64:\n> ",b64encode(fc1.getvalue()).decode())
    r.send(b64encode(fc2.getvalue())+b"\n")
print(r.recv(1024))
```

> 其实这个题的预期解被放到src里了。