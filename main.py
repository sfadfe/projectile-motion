import math
from function import *
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from fff import *

v0, theta = map(int, input().split())
Vx = v0 * math.cos(math.radians(theta))
Vy = v0 * math.sin(math.radians(theta))
t = eq1(0, Vy, -g) * 2
print(t)
h = eq2(t/2, Vy, -g)
print(h)
if type(t) != int:
    t = int(t)
frame = t*30

data = []
for i in range(frame + 1):
    Sx = eq2(i/30, Vx, 0)
    Sy = eq2(i/30, Vy, -g) if i <= frame / 2 else h - eq2(i/30 - frame/60, 0, g)
    data.append({'frame': i, 'Sx': Sx, 'Sy': Sy})

df = pd.DataFrame(data)
df.to_csv('result.csv', index=False)

plt.plot(df['Sx'], df['Sy'])
plt.savefig('result.png')

csv_path = 'result.csv'
x = 'Sx'
y = 'Sy'

animate()