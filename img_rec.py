# %% imports
import math
import cv2
import random
import numpy as np
import pytesseract
from functools import reduce

# %%
board = cv2.imread('board4.png')
N = 7

# %%
gray = cv2.cvtColor(board, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (15, 15), 0)
_, thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)
# %%
contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE,
                                       cv2.CHAIN_APPROX_SIMPLE)
# %%
cv2.imwrite('t.png', thresh)
# %%

shapes = [c for c in contours[2:] if np.sum((np.max(c, axis=0) - np.min(c, axis=0))**2) >= 50000]

# %%
vertices = np.empty((N+1, N+1, 2))
upper_left = np.min(contours[1], axis=0)
dists = ((np.max(contours[1], axis=0) - upper_left) / N)[0]
h = np.array([0, dists[1]])
v = np.array([dists[0], 0])
for i in range(N + 1):
    for j in range(N + 1):
        vertices[i, j] = np.round(upper_left + h * i + v * j)
midpoints = (vertices[1:, 1:] + vertices[:-1, :-1])/2

# %% Shapes
point_shape = [[] for _ in range(len(shapes))]

for k in range(len(shapes)):
    for i in range(N):
        for j in range(N):
            if cv2.pointPolygonTest(shapes[k], midpoints[i, j], False) > 0:
                point_shape[k].append([i, j])

# %% Shape texts
texts = [[] for _ in range(len(shapes))]
for k in range(len(shapes)):
    verts = point_shape[k]
    top = reduce(lambda m, v: min(m, v[0]), verts, N)
    left = reduce(lambda m, v: min(m, v[1] if v[0] == top else N), verts, N)

    assert top < N
    assert left < N

    y = math.floor(upper_left[0][0] + top * dists[0])
    x = math.floor(upper_left[0][1] + left * dists[1])

    img_part = board[(y+5):math.floor(y + 1/2*dists[0]), (x+5):math.floor(x+dists[1]-5)]
    texts[k] = pytesseract.image_to_string(img_part)
    cv2.imwrite(f'img_{k}.png', img_part)

# %%
texts
# %%

ss = board.copy()
for c in shapes:
    ss = cv2.drawContours(ss, [np.array(c).astype('int32')], 0, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 3)
# %%
cv2.imwrite('ss.png', ss)

# %%
