from function import *
import time
import pandas as pd
import math
from fff import *

theta = 0
fps = 60
data = []
v, r = map(int, input().split())
w = eq4(r, v)
theta_delta = eq5(w, 1/fps)
T = 2 * math.pi * r / w
T = int(T) +1
for i in range(T * fps + 1):
    x1 = r * math.cos(theta)
    y1 = r * math.sin(theta)
    data.append({'frame': i, 'x': x1, 'y': y1})
    theta += theta_delta

df = pd.DataFrame(data)
df.to_csv('output.csv', index=False)

points = load_points('output.csv', 'x', 'y')
norm_points, Wpx, Hpx = norm_circle(points, 80, 20, fps, isYminus=False)
last_frame = norm_points[-1][0]
grid = [[False]*Wpx for _ in range(Hpx)]
prev_px = prev_py = None
try:
    for f in range(last_frame + 1):
        for frame_id, px, py in norm_points:
            if frame_id == f:
                if prev_px is not None:
                    draw_line(grid, prev_px, prev_py, px, py, Hpx)
                else:
                    set_pixel(grid, px, py, Hpx)
                prev_px, prev_py = px, py
        a = draw_braille(grid, 80, 20)
        print("\033[2J\033[H", end='')
        print(f"Frame {f}/{last_frame}")
        print(a)
        time.sleep(0.5 / (fps * 0.76))
except KeyboardInterrupt:
    pass