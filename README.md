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
Note: This project has been tested with Python 3.10+.

## Configuration / Parameters
Parameters can be modified directly in ```main.py```:
| Parameter       | Description                     | Example |
|-----------------|---------------------------------|---------|
| grid_size       | Size of the 2D lattice (NxN)    | 100      |
| temperature     | Simulation temperature           | 2.5     |
| sweeps          | Number of Monte Carlo sweeps     | 1000    |
| output_folder   | Folder where PNG images are saved| data/ising_images |


## To Run the Script
Parameters such as grid size, temperature, and number of sweeps can be modified directly in ```main.py```.
To run the main script:
```bash
python3 main.py
```

## Output
PNGs will be created in the ```data```/```ising_images``` folder.

- Black = spin up (knit)
- White = spin down (purl)

These then can be uploaded to the Kniterate Editor.