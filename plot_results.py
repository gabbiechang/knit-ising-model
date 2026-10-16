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


def plot_comparison(run_folder, output_folder="plots"):
    """
    Compare Metropolis vs Wolff results (requires ising_results.csv and wolff_results.csv)
    """
    os.makedirs(output_folder, exist_ok=True)

    metro_csv = os.path.join(run_folder, "ising_results.csv")
    wolff_csv = os.path.join(run_folder, "wolff_results.csv")

    if not os.path.exists(metro_csv) or not os.path.exists(wolff_csv):
        print("Missing CSV files for comparison.")
        return

    df_metro = pd.read_csv(metro_csv)
    df_wolff = pd.read_csv(wolff_csv)

    # Group and average
    metro_stats = df_metro.groupby("temperature")["magnetization"].agg([np.mean, np.std])
    wolff_stats = df_wolff.groupby("temperature")["magnetization"].agg([np.mean, np.std])

    plt.figure(figsize=(8,6))
    plt.errorbar(metro_stats.index, np.abs(metro_stats["mean"]), yerr=metro_stats["std"],
                 fmt="o-", capsize=3, label="Metropolis")
    plt.errorbar(wolff_stats.index, np.abs(wolff_stats["mean"]), yerr=wolff_stats["std"],
                 fmt="s-", capsize=3, label="Wolff")

    plt.xlabel("Temperature T")
    plt.ylabel(r"$\langle |M| \rangle / N$")
    plt.title("Magnetization: Metropolis vs Wolff")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(output_folder, "magnetization_comparison.png"))
    plt.close()

    print(f"Comparison plot saved to {output_folder}")