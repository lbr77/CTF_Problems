import numpy as np
from PIL import Image
from secret import flag
from function import generate_points,generate_flag
from base64 import b64encode
r = np.array(generate_flag(flag).convert("RGB"))
w, h = r.shape[:2]
points = generate_points(6)
t = np.zeros_like(r)
r = r.reshape((w * h, 3))
for i in range(len(points)):
    y, x = points[i]
    t[x, w - 1 - y] = r[i]

Image.fromarray(np.array(t).reshape((w, h, 3))).save("gen.png")
print(b64encode(open("gen.png", "rb").read()).decode())
input()