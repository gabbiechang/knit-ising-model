import os
from ising import run_simulation
from image_utils import save_grid_image

def main():
    output_folder = "data/ising_images"
    os.makedirs(output_folder, exist_ok=True)

    N = 150
    sweeps = 1000
    temps = [0.01, 1.0, 1.5, 2.0, 2.27, 2.5, 3.0, 4.0]

    for T in temps:
        grid = run_simulation(N, T, sweeps, seed=42)
        filename = os.path.join(output_folder, f"ising_T{T:.2f}.png")
        save_grid_image(grid, filename)
        print(f"Saved {filename}")

if __name__ == "__main__":
    main()