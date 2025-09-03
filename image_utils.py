from PIL import Image
import numpy as np
import os

def save_grid_image(grid, filename):
    """
    Save a grid of spins (-1, +1) as a binary PNG where +1 is black and -1 is white.
    Adds borders and extra rows for knitting patterns.
    """
    img_array = np.where(grid == 1, 0, 255).astype(np.uint8)  # 1=black, -1=white
    img = Image.fromarray(img_array, mode="L")
    grid = add_rice_stitch_border(grid, border_width=20)
    grid = add_top_bottom_rows(grid, num_rows=20)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    img.save(filename)

    # Map spins -1 → white (255), +1 → black (0)
    img_array = np.where(grid == 1, 0, 255).astype(np.uint8)
    img = Image.fromarray(img_array, mode='L')

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    img.save(filename)

def add_rice_stitch_border(grid, border_width=10):
    """
    Add a rice stitch (checkerboard) border to all four edges of the grid,
    including corners.
    """
    N = grid.shape[0]
    bordered = grid.copy()
    for i in range(N):
        for j in range(N):
            if i < border_width or i >= N - border_width or j < border_width or j >= N - border_width:
                bordered[i, j] = 1 if (i + j) % 2 == 0 else -1
    return bordered


def add_top_bottom_rows(grid, num_rows=20):
    """
    Add `num_rows` rows of knits to the top and bottom of the grid.
    """
    rows = np.ones((num_rows, grid.shape[1]), dtype=int)
    return np.vstack([rows, grid, rows])
