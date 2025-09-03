# Knit Ising Model

This project simulates the 2D Ising model using the Metropolis Monte Carlo algorithm and produces binary 
PNGs that can be imported into Kniterate's Stitch Image tool for knitting.

## To Run

```bash
pip install -r requirements.txt
python3 main.py
```

## Output
A black-and-white PNG will be created in the data/ folder.

- Black = spin up (knit)
- White = spin down (purl/rear bed)

Upload this image to Kniterate Editor and assign stitch types accordingly.