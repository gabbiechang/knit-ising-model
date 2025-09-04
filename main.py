import os
import numpy as np
import csv
from datetime import datetime
from ising import run_simulation, compute_magnetization, compute_energy
from image_utils import save_grid_image

def main():
    # Make a unique run folder with timestamp
    run_id = datetime.now().strftime("ising_run_%Y%m%d_%H%M%S")
    run_folder = os.path.join("data", run_id)
    output_folder = os.path.join(run_folder, "ising_images")
    os.makedirs(output_folder, exist_ok=True)

    N = 150
    sweeps = 1000
    temps = [0.01, 1.0, 1.5, 2.0, 2.27, 2.5, 3.0, 4.0]
    num_realizations = 10

    csv_file = os.path.join(run_folder, "ising_results.csv")
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["temperature", "realization", "seed", "magnetization", "energy"])

        for T in temps:
            for r in range(num_realizations):
                seed = np.random.randint(0, 1_000_000)   # pick a new seed each time
                grid = run_simulation(N, T, sweeps, seed=seed)

                mag = compute_magnetization(grid)
                energy = compute_energy(grid)

                writer.writerow([T, r, seed, mag, energy])

                filename = os.path.join(output_folder, f"ising_T{T:.2f}_r{r}_seed{seed}.png")
                save_grid_image(grid, filename)
                print(f"Saved {filename}")

if __name__ == "__main__":
    main()