import time
from fff import *
import math
from function import *
import pandas as pd
import math

fps = 144
frame = 0
csv_path = '1234.csv'

v0, r0 = map(int, input().split())
theta = 0
d_r = 15

data = []
w = eq4(r0, v0) # 각속도 값은 고정할거임
d_theta = eq5(w, 1/fps)

while theta <= math.radians(720):
    x1 = r0 * math.cos(theta)
    y1 = r0 * math.sin(theta)
    data.append({'frame': frame, 'x': x1, 'y': y1})
    frame += 1
    theta += d_theta
    r0 += d_r
    print(f'{math.degrees(theta):.2f} / 720')

df = pd.DataFrame(data)
df.to_csv(csv_path, index=False)

R_max = ((df['x']**2 + df['y']**2)**0.5).max() or 1.0
height_cells = int(4* math.sqrt(R_max))
height_cells = max(14, min(80, height_cells))
width_cells = max(14, min(80, height_cells))

points = load_points(csv_path, 'x', 'y')
fr0, x0, y0 = points[0]
point = [(f, x - x0, y - y0) for f, x, y in points]
norm_points, Wpx, Hpx = norm_spiral(point, width_cells, height_cells, padding=0.05)
last_frame = norm_points[-1][0]
grid = [[False]*Wpx for _ in range(Hpx)]
prev_px = prev_py = None
try:
    for f, px, py in norm_points:
        if prev_px is not None:
            draw_line(grid, prev_px, prev_py, px, py, Hpx)
        else:
            set_pixel(grid, px, py, Hpx)
        prev_px, prev_py = px, py
        a = draw_braille(grid, Hpx, Wpx)
        print("\033[2J\033[H", end='')
        print(f"Frame {f}/{last_frame}")
        print(a)
        time.sleep(0.5 / (fps * 1))
except KeyboardInterrupt:
    pass