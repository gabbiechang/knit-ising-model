import os
import numpy as np
import csv
import plot_results
from datetime import datetime
from ising import run_simulation, compute_magnetization, compute_energy
from image_utils import save_grid_image
from concurrent.futures import ProcessPoolExecutor

def worker(args):
    T, r, N, steps, output_folder = args
    seed = np.random.randint(0, 1000000)
    grid = run_simulation(N, T, steps, seed)

    mag = compute_magnetization(grid)
    energy = compute_energy(grid)

    filename = os.path.join(output_folder, f"ising_T{T:.2f}_r{r}_seed{seed}.png")
    save_grid_image(grid, filename)
    print(f"Saved {filename}")

    return (T, r, seed, mag, energy)

def main():
    run_id = datetime.now().strftime("ising_run_%Y%m%d_%H%M%S")
    run_folder = os.path.join("data", run_id)
    output_folder = os.path.join(run_folder, "ising_images")
    os.makedirs(output_folder, exist_ok=True)

    N = 150
    steps = N*N*10000
    temps = [0.00000000001, 0.01, 1.0, 1.5, 2.0, 2.27, 2.5, 3.0, 4.0]
    num_realizations = 10

    csv_file = os.path.join(run_folder, "ising_results.csv")

    tasks = [(T, r, N, steps, output_folder) for T in temps for r in range(num_realizations)]

    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        results = list(executor.map(worker, tasks))

    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["temperature", "realization", "seed", "magnetization", "energy"])
        writer.writerows(results)

    plots_folder = os.path.join(run_folder, "plots")
    plot_results.plot_ising_results(csv_file, output_folder=plots_folder)

if __name__ == "__main__":
    main()