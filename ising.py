import numpy as np
from numba import njit

def initial_grid(N, seed=None):
    if seed is not None:
        np.random.seed(seed)
    # Generate 0 or 1 and map to -1 or +1
    return 2 * np.random.randint(0, 2, size=(N, N)) - 1

@njit
def metropolis_sweep(grid, T):
    N = grid.shape[0]
    for _ in range(N * N):
        i = np.random.randint(0, N)
        j = np.random.randint(0, N)
        spin = grid[i, j]
        neighbors = (
            grid[(i+1) % N, j] +
            grid[(i-1) % N, j] +
            grid[i, (j+1) % N] +
            grid[i, (j-1) % N]
        )
        delta_E = 2 * spin * neighbors
        if delta_E <= 0 or np.random.rand() < np.exp(-delta_E / T):
            grid[i, j] *= -1
    return grid


def run_simulation(N, T, sweeps, seed=None):
    grid = initial_grid(N, seed)
    for _ in range(sweeps):
        metropolis_sweep(grid, T)
    return grid

def compute_magnetization(grid):
    return np.mean(grid)

def compute_energy(grid):
    N = grid.shape[0]
    energy = 0
    for i in range(N):
        for j in range(N):
            spin = grid[i, j]
            neighbors = (
                grid[(i+1)%N, j] +
                grid[i, (j+1)%N]
            )
            energy -= spin * neighbors
    return energy / (N * N)