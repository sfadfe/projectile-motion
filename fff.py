import time
import pandas as pd

def load_points(csv_path, x_col, y_col):
    df = pd.read_csv(csv_path)
    frames = df['frame'].tolist() if 'frame' in df.columns else list(range(len(df)))
    xs = df[x_col].tolist()
    ys = df[y_col].tolist()
    return list(zip(frames, xs, ys))

def norm_circle(points, width_cells, height_cells, fps, padding=0.07, floor_zero=False):
    xs = [x for _, x, _ in points]
    ys = [y for _, _, y in points]
    xmin, xmax = min(xs), max(xs)
    if floor_zero:
        ymin = 0
        ymax = max(ys)
    else:
        ymin, ymax = min(ys), max(ys)
    dx = xmax - xmin or 1
    dy = ymax - ymin or 1
    xmin -= dx * padding
    xmax += dx * padding
    ymin -= dy * padding
    ymax += dy * padding
    dx = xmax - xmin
    dy = ymax - ymin
    Wpx = width_cells * 2
    Hpx = height_cells * 4
    norm_points = []
    for f, x, y in points:
        px = (x - xmin) / dx * (Wpx - 1)
        py = (y - ymin) / dy * (Hpx - 1)
        norm_points.append((f, px, py))
    return norm_points, Wpx, Hpx

DOT_MAP = {
    (0,0): 1, (0,1): 2, (0,2): 3, (0,3): 7,
    (1,0): 4, (1,1): 5, (1,2): 6, (1,3): 8,
}

def draw_braille(grid, width_cells, height_cells):
    Wpx = width_cells * 2
    Hpx = height_cells * 4
    lines = []
    for cy in range(height_cells):
        row = []
        for cx in range(width_cells):
            bits = 0
            for dy in range(4):
                for dx in range(2):
                    gy = cy*4 + dy
                    gx = cx*2 + dx
                    if grid[gy][gx]:
                        bits |= 1 << (DOT_MAP[(dx, dy)] - 1)
            row.append(chr(0x2800 + bits) if bits else ' ')
        lines.append(''.join(row))
    return '\n'.join(lines)

def set_pixel(grid, x, y, Hpx):
    ix = int(round(x))
    iy = int(round(y))
    if 0 <= ix < len(grid[0]) and 0 <= iy < Hpx:
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

def norm1(points, width_cells, height_cells, fps, padding=0.07, floor_zero=False, shift_x=True):
    xs = [x for _, x, _ in points]
    ys = [y for _, _, y in points]
    if floor_zero and min(ys) >= 0:
        ymin, ymax = 0, max(ys)
    else:
        ymin, ymax = min(ys), max(ys)
    xmin_raw, xmax_raw = min(xs), max(xs)
    shift = -xmin_raw if (shift_x and xmin_raw < 0) else 0
    xs_shifted = [x + shift for x in xs]
    xmin, xmax = min(xs_shifted), max(xs_shifted)
    dx = xmax - xmin
    dy = ymax - ymin
    if dx == 0: dx = 1
    if dy == 0: dy = 1
    xmin -= dx * padding
    xmax += dx * padding
    ymin -= dy * padding
    ymax += dy * padding
    dx = xmax - xmin
    dy = ymax - ymin
    if dx == 0: dx = 1
    if dy == 0: dy = 1
    Wpx = width_cells * 2
    Hpx = height_cells * 4
    norm_points = []
    for idx, (f, _x, y) in enumerate(points):
        x_use = xs_shifted[idx]
        px = (x_use - xmin) / dx * (Wpx - 1)
        py = (y - ymin) / dy * (Hpx - 1)
        norm_points.append((f, px, py))
    return norm_points, Wpx, Hpx



def animate(csv_path, x_col, y_col, width_cells, height_cells, fps, floor_zero=False):
    points = load_points(csv_path, x_col, y_col)
    norm_points, Wpx, Hpx = norm1(points, width_cells, height_cells, fps, floor_zero=floor_zero)
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

def animate_circle(csv_path, x_col, y_col, width_cells, height_cells, fps, floor_zero=False):
    points = load_points(csv_path, x_col, y_col)
    norm_points, Wpx, Hpx = norm_circle(points, width_cells, height_cells, fps, floor_zero=floor_zero)
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