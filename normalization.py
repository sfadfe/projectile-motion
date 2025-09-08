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

def norm1(points, width_cells, height_cells, fps, padding=0.07, floor_zero=False, shift_x=True):
    xs = [x for _, x, _ in points]
    ys = [y for _, _, y in points]
    if floor_zero and min(ys) >= 0:
        ymin, ymax = 0, max(ys)
    else:
        ymin, ymax = min(ys), max(ys)
    xmin, xmax = min(xs), max(xs)
    shift = -xmin if (shift_x and xmin < 0) else 0
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

def norm_spiral(points, width_cells, height_cells, padding=0.05, y_compensate=True):
    if not points:
        return [], width_cells*2, height_cells*4
    
    f0, x0, y0 = points[0]
    work = [(f, x - x0, y - y0) for f, x, y in points]
    
    xs = [x for _, x, _ in work]
    ys = [y for _, _, y in work]
    R = max(abs(min(xs)), abs(max(xs)), abs(min(ys)), abs(max(ys))) or 1.0
    xmin, xmax = -R, R
    ymin, ymax = -R, R
    xmin -= R * padding
    xmax += R * padding
    ymin -= R * padding
    ymax += R * padding
    dx = xmax - xmin or 1.0
    dy = ymax - ymin or 1.0
    Wpx = width_cells * 2
    Hpx = height_cells * 4
    norm_points = []
    for f, x, y in work:
        px = (x - xmin) / dx * (Wpx - 1)
        if y_compensate:
            py = (y - ymin) / dy * (Hpx - 1) * 0.24
        else:
            py = (y - ymin) / dy * (Hpx - 1)
        norm_points.append((f, px, py))
    return norm_points, Wpx, Hpx