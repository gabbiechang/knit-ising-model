import numpy as np
from PIL import Image

def initialize_grid(size):
    return np.random.choice([-1, 1], size=(size, size))

def metropolis_step(grid, T):
    N = grid.shape[0]
    for _ in range(N**2):
        i, j = np.random.randint(0, N, size=2)
        s = grid[i, j]
        neighbors = grid[(i+1)%N, j] + grid[i, (j+1)%N] + grid[(i-1)%N, j] + grid[i, (j-1)%N]
        delta_E = 2 * s * neighbors
        if delta_E < 0 or np.random.rand() < np.exp(-delta_E / T):
            grid[i, j] *= -1
    return grid

def spins_to_image(grid, filename):
    # Convert +1 → black (0), -1 → white (255)
    img_array = np.uint8((1 - grid) * 127.5)
    img = Image.fromarray(img_array)
    img.save(filename)

# Run it
size = 100
T = 2.0
grid = initialize_grid(size)

for _ in range(100):  # burn-in period
    grid = metropolis_step(grid, T)

spins_to_image(grid, f'ising_T{T}.png')