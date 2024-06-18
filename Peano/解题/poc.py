import numpy as np
from base64 import b64decode
import io
from pwn import *
from PIL import Image
p = remote('localhost',5000)
r = b64decode(p.recvline().strip())
r = Image.open(io.BytesIO(r)).convert("RGB")
r.save("recv.png")
r = np.array(r)

def peano_curve(n):
    peano_old = np.array([[0, 0], [0, 1], [0.5, 1], [0.5, 0], [1, 0], [1, 1]])
    points = peano_old.tolist()
    # points = []
    for i in range(1, n):
        p1 = np.column_stack((peano_old[:, 0], 2 + 1 / (3**i - 1) - peano_old[:, 1]))
        p1 = p1[::-1]
        p2 = np.column_stack((p1[:, 0], 4 + 3 / (3**i - 1) - p1[:, 1]))
        p2 = p2[::-1]
        peano_new = np.vstack((peano_old, p1, p2))
        p1 = np.column_stack((2 + 1 / (3**i - 1) - peano_new[:, 0], peano_new[:, 1]))
        p1 = p1[::-1]
        p2 = np.column_stack((4 + 3 / (3**i - 1) - p1[:, 0], p1[:, 1]))
        p2 = p2[::-1]
        peano_new = np.vstack((peano_new, p1, p2))
        peano_old = peano_new / (3 + 2 / (3**i - 1))
        points = peano_old.tolist()
    points = np.round(np.array(points) * (3**n - 1)).astype(int)
    nP = []
    for i in range(len(points) - 1):
        nP.append(points[i])
        dx = int(points[i + 1][0] - points[i][0])
        dy = int(points[i + 1][1] - points[i][1])
        if dx == 0:
            for j in range(1, abs(dy)):
                nP.append(np.array([points[i][0], points[i][1] + j * (dy // abs(dy))]))
        else:
            for j in range(1, abs(dx)):
                nP.append(np.array([points[i][0] + j * (dx // abs(dx)), points[i][1]]))
    nP.append(points[-1])
    return np.array(nP)

points = peano_curve(6)
w, h = r.shape[:2]
s = []
for i in range(len(points)):
    y, x = points[i]
    s.append(r[x, w - 1 - y])
Image.fromarray(np.array(s).reshape((h, w, 3))).save("decrypted.png")