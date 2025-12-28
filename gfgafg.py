import matplotlib.pyplot as plt

y = [0.5, 4.41, 1, 0.9, 0.9, 0.7, 0.5, 0.48, 0.37, 0.36]
x = [1960, 1966, 1975, 1985, 1995, 2005, 2015, 2020, 2024, 2025]

plt.plot(x, y)
plt.ylabel('Ratio')
plt.xlabel('Year')
plt.title('NASA’s budget ratio to the federal budget')
plt.grid()
plt.show()
