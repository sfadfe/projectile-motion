import math
from function import *
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from fff import *

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

plt.plot(df['Sx'], df['Sy'])
plt.savefig('result.png')

csv_path = 'result.csv'
x = 'Sx'
y = 'Sy'
min_width_cell = 24 * (1+(Sx_max/100))
width_cells =  min(100, max(int(24 * (1+(Sx_max/100))), int(Sx_max/2)))
height_cells = min(20, int(10*math.sqrt(h)))
animate(csv_path, x, y, width_cells, height_cells, fps)
print(t)
print(h)