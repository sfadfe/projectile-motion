import math
import time
from function import *
import pandas as pd
from fff import *
from normalization import *

fps = 150
v0, theta = map(int, input().split())
Vx = v0 * math.cos(math.radians(theta))
Vy = v0 * math.sin(math.radians(theta))
if theta == 90:
    Vx = 0
t = eq1(0, Vy, -g)
h = eq2(t, Vy, -g)
frame = math.ceil(t * fps * 2)  #현재로썬 이 방법이 최선. t가 작아지면 구현이 안됨. 최소 상승 프레임 구현은 프로젝트 목적에 안맞음.

data = []
for i in range(frame):
    sec = i/fps
    Sx = eq2(sec, Vx, 0)
    Sy = eq2(sec, Vy, -g) if sec <= t*2  else h - eq2(sec - t, 0, g)
    data.append({'frame': i, 'Sx': Sx, 'Sy': Sy})

last_sec = frame/fps
Sx = eq2(last_sec, Vx, 0)
Sx_max = abs(Sx)
Sy = 0
data.append({'frame': i, 'Sx': Sx, 'Sy': Sy})

df = pd.DataFrame(data)
df.to_csv('result.csv', index=False)

csv_path = 'result.csv'
x = 'Sx'
y = 'Sy'
min_width_cell = 24 * (1+(Sx_max/100))
width_cells =  min(100, max(int(24 * (1+(Sx_max/100))), int(Sx_max/2)))
height_cells = min(20, int(10*math.sqrt(h)))

points = load_points(csv_path, x, y)
norm_points, Wpx, Hpx = norm1(points, width_cells, height_cells, fps, floor_zero=False)
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
        a = draw_braille(grid, width_cells, height_cells)
        print("\033[2J\033[H", end='')
        print(f"Frame {f}/{last_frame}")
        print(a)
        time.sleep(0.5 / (fps * 1))
except KeyboardInterrupt:
    pass

print(t)
print(h)