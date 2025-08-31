from function import *
import pandas as pd
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import fff

theta = 0
frame = 60
data = []
v, r = map(int, input().split())
w = eq4(r, v)
theta_delta = eq5(w, 1/frame)
T = 2 * math.pi * r / w
T = int(T) +1
for i in range(T * frame + 1):
    x1 = r * math.cos(theta)
    y1 = r * math.sin(theta)
    data.append({'frame': i, 'x': x1, 'y': y1})
    theta += theta_delta

df = pd.DataFrame(data)
df.to_csv('output.csv', index=False)
plt.plot(df['x'], df['y'])
plt.savefig('result1.png')

fff.animate('output.csv', 'x', 'y')