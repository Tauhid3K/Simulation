import numpy as np

# 1. Generate data
inter_arrival = np.random.uniform(0, 10, 1000)
service_times = np.random.uniform(2, 8, 1000)

# 2. Sample statistics
sample_arr_mean, sample_arr_std = np.mean(inter_arrival), np.std(inter_arrival, ddof=1)
sample_ser_mean, sample_ser_std = np.mean(service_times), np.std(service_times, ddof=1)

# 3. Theoretical values
theo_arr_mean, theo_arr_std = 5.0, (10 - 0) / np.sqrt(12)
theo_ser_mean, theo_ser_std = 5.0, (8 - 2) / np.sqrt(12)

# 4. Display comparison
print("--- Inter-Arrival Times (0 to 10 min) ---")
print(f"Sample Mean    : {sample_arr_mean:.4f}  | Theoretical: {theo_arr_mean:.4f}")
print(f"Sample Std Dev : {sample_arr_std:.4f}  | Theoretical: {theo_arr_std:.4f}")

print("\n--- Service Times (2 to 8 min) ---")
print(f"Sample Mean    : {sample_ser_mean:.4f}  | Theoretical: {theo_ser_mean:.4f}")
print(f"Sample Std Dev : {sample_ser_std:.4f}  | Theoretical: {theo_ser_std:.4f}")

# 5. Plot all simulation results
try:
    import matplotlib
    import matplotlib.pyplot as plt
    import subprocess

    fig, axes = plt.subplots(2, 3, figsize=(16, 9))

    axes[0, 0].hist(inter_arrival, bins=20, density=True, edgecolor="black", color="skyblue", alpha=0.8)
    axes[0, 0].axhline(1 / 10, color="navy", linestyle="--", label="Theoretical density")
    axes[0, 0].axvline(sample_arr_mean, color="red", linestyle="--", label=f"Sample mean: {sample_arr_mean:.2f}")
    axes[0, 0].set_title("Inter-Arrival Distribution")
    axes[0, 0].set_xlabel("Minutes")
    axes[0, 0].set_ylabel("Probability density")
    axes[0, 0].legend()

    axes[0, 1].hist(service_times, bins=20, density=True, edgecolor="black", color="lightgreen", alpha=0.8)
    axes[0, 1].axhline(1 / 6, color="darkgreen", linestyle="--", label="Theoretical density")
    axes[0, 1].axvline(sample_ser_mean, color="red", linestyle="--", label=f"Sample mean: {sample_ser_mean:.2f}")
    axes[0, 1].set_title("Service-Time Distribution")
    axes[0, 1].set_xlabel("Minutes")
    axes[0, 1].set_ylabel("Probability density")
    axes[0, 1].legend()

    axes[0, 2].plot(np.sort(inter_arrival), np.arange(1, len(inter_arrival) + 1) / len(inter_arrival),
                    color="steelblue", label="Inter-arrival")
    axes[0, 2].plot(np.sort(service_times), np.arange(1, len(service_times) + 1) / len(service_times),
                    color="seagreen", label="Service")
    axes[0, 2].set_title("Cumulative Distributions")
    axes[0, 2].set_xlabel("Minutes")
    axes[0, 2].set_ylabel("Cumulative probability")
    axes[0, 2].grid(alpha=0.3)
    axes[0, 2].legend()

    sample_numbers = np.arange(1, len(inter_arrival) + 1)
    axes[1, 0].plot(sample_numbers, np.cumsum(inter_arrival) / sample_numbers, color="steelblue",
                    label="Inter-arrival mean")
    axes[1, 0].plot(sample_numbers, np.cumsum(service_times) / sample_numbers, color="seagreen",
                    label="Service mean")
    axes[1, 0].axhline(5, color="black", linestyle="--", label="Theoretical mean: 5")
    axes[1, 0].set_title("Running Sample Means")
    axes[1, 0].set_xlabel("Number of observations")
    axes[1, 0].set_ylabel("Mean (minutes)")
    axes[1, 0].legend()

    axes[1, 1].boxplot([inter_arrival, service_times], tick_labels=["Inter-arrival", "Service"])
    axes[1, 1].set_title("Spread and Outliers")
    axes[1, 1].set_ylabel("Minutes")
    axes[1, 1].grid(axis="y", alpha=0.3)

    labels = ["Arrival mean", "Service mean", "Arrival std", "Service std"]
    values = [sample_arr_mean, sample_ser_mean, sample_arr_std, sample_ser_std]
    bars = axes[1, 2].bar(labels, values, color=["skyblue", "lightgreen", "cornflowerblue", "mediumseagreen"])
    axes[1, 2].set_title("Sample vs Theoretical Statistics")
    axes[1, 2].set_ylabel("Minutes")
    axes[1, 2].tick_params(axis="x", rotation=25)
    axes[1, 2].bar_label(bars, fmt="%.3f", padding=3)

    fig.suptitle("Arrival and Service Time Simulation", fontsize=16)
    fig.tight_layout()
    output_file = "arrival_service_histograms.png"
    fig.savefig(output_file, dpi=150)
    print(f"\nGraph successfully saved to '{output_file}'")

    backend = matplotlib.get_backend().lower()
    if backend == "agg":
        # In headless / Agg mode, plt.show() cannot open a window.
        # Open the generated image directly using the system viewer.
        try:
            subprocess.Popen(["xdg-open", output_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"Opened '{output_file}' in default image viewer.")
        except Exception:
            print(f"Open '{output_file}' to view the plot.")
    else:
        plt.show()
except ImportError:
    print("\n[!] Error: 'matplotlib' is not installed, so the graph cannot be generated.")
    print("    Install it using:")
    print("      sudo pacman -S python-matplotlib")
    print("    or:")
    print("      pip install --user matplotlib --break-system-packages")
