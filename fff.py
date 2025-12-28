import pandas as pd
from normalization import *

def load_points(csv_path, x, y):
    df = pd.read_csv(csv_path)
    frames = df['frame'].tolist() if 'frame' in df.columns else list(range(len(df)))
    xs = df[x].tolist()
    ys = df[y].tolist()
    return list(zip(frames, xs, ys))

DOT_MAP = {
    (0,0): 1, (0,1): 2, (0,2): 3, (0,3): 7,
    (1,0): 4, (1,1): 5, (1,2): 6, (1,3): 8,
}

def draw_braille(grid, Wpx, Hpx):
    if not grid:
        return ""
    H_real = len(grid)
    W_real = len(grid[0]) if H_real > 0 else 0
    cell_rows = H_real // 4
    cell_cols = W_real // 2
    if cell_rows == 0 or cell_cols == 0:
        return ""
    lines = []
    for cy in range(cell_rows):
        row = []
        for cx in range(cell_cols):
            bits = 0
            for dy in range(4):
                for dx in range(2):
                    gy = cy * 4 + dy
                    gx = cx * 2 + dx
                    if 0 <= gy < H_real and 0 <= gx < W_real and grid[gy][gx]:
                        dot_idx = DOT_MAP.get((dx, dy), 0)
                        if dot_idx > 0:
                            bits |= 1 << (dot_idx - 1)
            row.append(chr(0x2800 + bits) if bits else ' ')
        lines.append(''.join(row))
    return '\n'.join(lines)

def set_pixel(grid, x, y, Hpx):
    if not grid:
        return
    ix = int(round(x))
    iy = int(round(y))
    if 0 <= iy < Hpx and 0 <= ix < len(grid[0]):
        grid[Hpx - 1 - iy][ix] = True

def draw_line(grid, x0, y0, x1, y1, Hpx):
    x0 = int(round(x0)); y0 = int(round(y0))
    x1 = int(round(x1)); y1 = int(round(y1))
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        set_pixel(grid, x0, y0, Hpx)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy