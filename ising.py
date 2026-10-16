import numpy as np
from numba import njit

def initial_grid(N, seed):
    np.random.seed(seed) # TODO: investigate if we need to record this random num generator state
    # Generate 0 or 1 and map to -1 or +1
    return (2 * np.random.randint(0, 2, size=(N, N))) - 1

@njit
def metropolis_sweep(grid, T, steps):
    N = grid.shape[0]
    for _ in range(steps):
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

@njit
def wolff_update(grid, T):
    """
    Perform one Wolff cluster update on the Ising grid.
    """
    N = grid.shape[0]
    # pick random seed spin
    i = np.random.randint(0, N)
    j = np.random.randint(0, N)
    spin = grid[i, j]

    # probability to add aligned neighbor
    p_add = 1 - np.exp(-2.0 / T)

    # cluster growth (stack-based)
    cluster = [(i, j)]
    in_cluster = np.zeros((N, N), dtype=np.uint8)
    in_cluster[i, j] = 1

    while cluster:
        x, y = cluster.pop()
        # four neighbors
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx = (x + dx) % N
            ny = (y + dy) % N
            if in_cluster[nx, ny] == 0 and grid[nx, ny] == spin:
                if np.random.rand() < p_add:
                    in_cluster[nx, ny] = 1
                    cluster.append((nx, ny))

    # flip entire cluster
    for x in range(N):
        for y in range(N):
            if in_cluster[x, y]:
                grid[x, y] *= -1

    return grid

def run_simulation(N, T, steps, seed):
    grid = initial_grid(N, seed)
    metropolis_sweep(grid, T, steps)
    return grid

def run_wolff_simulation(N, T, sweeps, seed):
    np.random.seed(seed)
    grid = initial_grid(N, seed)
    for _ in range(sweeps):
        grid = wolff_update(grid, T)
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
                grid[i, (j+1)%N] +
                grid[(i-1)%N, j] +
                grid[i, (j-1)%N]
            )
            energy -= spin * neighbors
    return energy / (N * N)