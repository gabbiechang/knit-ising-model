# Knit Ising Model

This project simulates the 2D Ising model using the Metropolis Monte Carlo algorithm and produces binary 
PNGs that can be imported into Kniterate's Stitch Image tool for knitting.


## Installation

You should use a Python virtual environment to avoid conflicts with system packages.

1. Clone the repository:

```bash
git clone https://github.com/gabbiechang/knit-ising-model.git
cd knit-ising-model
```
2. Create a virtual environment:

```bash
python3 -m venv venv
```

3. Activate the virtual environment:

    For macOS / Linux:
    ```bash
    source venv/bin/activate
    ```
    For Windows (PowerShell):
    ```bash
    .\venv\Scripts\Activate.ps1
    ```

4. Install required packages:
```bash
pip install -r requirements.txt
```

5. To Run the Script:
Parameters such as grid size, temperature, and number of sweeps can be modified directly in `main.py`.
```bash
python3 main.py
```
You can optionally specify the number of CPU cores to use for parallel execution using the `--cores` flag.  
If not specified, the program will use all available cores by default.
```bash
python3 main.py --cores 8
```

## Configuration / Parameters
Parameters can be modified directly in `main.py`:

| Parameter           | Description                                                                 | Example |
|---------------------|-----------------------------------------------------------------------------|---------|
| N                   | Size of the 2D lattice (NxN)                                               | 150     |
| sweeps              | Number of Monte Carlo sweeps per simulation                                 | 1000    |
| temps               | List of temperatures to simulate                                            | [0.01, 1.0, 2.0, 2.27, 3.0] |
| num_realizations    | Number of independent simulations per temperature. Each realization has a unique random seed| 10      |
| output_folder       | Folder where data from each run will be saved                                       | data/ising_run_20250904_092635 |
| seed                | Optional random seed for reproducibility (one is generated per realization)| None    |
| csv_file            | CSV file path to store magnetization and energy for each realization        | ising_results.csv |

### Notes
- PNG filenames include the temperature, realization index, and seed, e.g., `ising_T2.27_r3_seed123456.png`.  
- Statistical properties (magnetization, energy) are logged in `data`/`csv_file`.

## Output
PNGs will be created in the `data`/`ising_images` folder.

- Black = spin up (knit)
- White = spin down (purl)

These then can be uploaded to the Kniterate Editor.