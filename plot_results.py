import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def plot_ising_results(csv_file, output_folder="plots"):
    os.makedirs(output_folder, exist_ok=True)

    # Load results
    df = pd.read_csv(csv_file)
    df["abs_magnetization"] = df["magnetization"].abs()

    grouped = df.groupby("temperature")

    temps = []
    mag_mean, mag_std = [], []
    energy_mean, energy_std = [], []

    for T, group in grouped:
        temps.append(T)
        mag_mean.append(group["abs_magnetization"].mean())
        mag_std.append(group["abs_magnetization"].std())
        energy_mean.append(group["energy"].mean())
        energy_std.append(group["energy"].std())

    temps = np.array(temps)

    # --- Magnetization plot ---
    plt.figure(figsize=(7,5))
    for T, group in grouped:
        plt.scatter([T]*len(group), group["abs_magnetization"], alpha=0.4, s=20)
    plt.errorbar(temps, mag_mean, yerr=mag_std, fmt="-o", capsize=3, label="Simulation avg")

    # Expected Onsager approx
    T_fit = np.linspace(min(temps), max(temps), 200)
    Tc = 2.27
    m_expected = np.where(T_fit < Tc, np.clip(1 - (T_fit/Tc)**8, 0, 1)**0.125, 0)
    plt.plot(T_fit, m_expected, "r--", label="Expected (Onsager 2D)")

    plt.xlabel("Temperature T")
    plt.ylabel(r"$\langle |M| \rangle / N$")
    plt.title("Magnetization vs Temperature")
    plt.legend()
    plt.savefig(os.path.join(output_folder, "magnetization_vs_T.png"))
    plt.close()

    # --- Energy plot ---
    plt.figure(figsize=(7,5))
    for T, group in grouped:
        plt.scatter([T]*len(group), group["energy"], alpha=0.4, s=20)
    plt.errorbar(temps, energy_mean, yerr=energy_std, fmt="-o", capsize=3, label="Simulation avg")

    plt.xlabel("Temperature T")
    plt.ylabel(r"$\langle E \rangle / N$")
    plt.title("Energy vs Temperature")
    plt.legend()
    plt.savefig(os.path.join(output_folder, "energy_vs_T.png"))
    plt.close()

    print(f"Plots saved to {output_folder}")
