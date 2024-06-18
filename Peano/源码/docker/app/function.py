import numpy as np
from PIL import Image
import qrcode
import qrcode.constants
def generate_points(n:int)->list:
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

def generate_flag(flag:str)->Image:
    qr = qrcode.QRCode(
        version=15,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=9,
        border=2,
    )
    qr.add_data(flag)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img