import os
import numpy as np
import csv
import plot_results
from datetime import datetime
from ising import run_simulation, compute_magnetization, compute_energy, run_wolff_simulation
from image_utils import save_grid_image
from concurrent.futures import ProcessPoolExecutor

N = 100
STEPS = N*N*1000
WOLFF_STEPS = 10000
TEMPS = [2.25, 2.3]
NUM_REALIZATIONS = 10

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

def wolff_worker(args):
    T, r, N, wolff_steps, output_folder = args
    seed = np.random.randint(0, 1000000)
    grid = run_wolff_simulation(N, T, wolff_steps, seed)

    mag = compute_magnetization(grid)
    energy = compute_energy(grid)

    filename = os.path.join(output_folder, f"wolff_T{T:.2f}_r{r}_seed{seed}.png")
    save_grid_image(grid, filename)
    print(f"Wolff saved {filename}")

    return (T, r, seed, mag, energy)

def main():
    run_id = datetime.now().strftime("ising_run_%Y%m%d_%H%M%S")
    run_folder = os.path.join("data", run_id)
    output_folder = os.path.join(run_folder, "ising_images")
    os.makedirs(output_folder, exist_ok=True)

    csv_file = os.path.join(run_folder, "ising_results.csv")

    tasks = [(T, r, N, STEPS, output_folder) for T in TEMPS for r in range(NUM_REALIZATIONS)]

    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        results = list(executor.map(worker, tasks))

    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["temperature", "realization", "seed", "magnetization", "energy"])
        writer.writerows(results)

    plots_folder = os.path.join(run_folder, "plots")
    plot_results.plot_ising_results(csv_file, output_folder=plots_folder)


    # TODO
    wolff_folder = os.path.join(run_folder, "wolff_results")
    os.makedirs(wolff_folder, exist_ok=True)
    wolff_csv = os.path.join(run_folder, "wolff_results.csv")

    wolff_tasks = [(T, r, N, WOLFF_STEPS, wolff_folder) for T in TEMPS for r in range(NUM_REALIZATIONS)]

    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        wolff_results = list(executor.map(wolff_worker, wolff_tasks))

    with open(wolff_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["temperature", "realization", "seed", "magnetization", "energy"])
        writer.writerows(wolff_results)

    wolff_plots_folder = os.path.join(run_folder, "wolff_plots")

    plot_results.plot_ising_results(csv_file, output_folder=plots_folder)
    plot_results.plot_ising_results(wolff_csv, output_folder=wolff_plots_folder)

    # automatic comparison plot
    compare_folder = os.path.join(run_folder, "comparison_plots")
    plot_results.plot_comparison(run_folder, output_folder=compare_folder)


if __name__ == "__main__":
    main()