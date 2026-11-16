import numpy as np
import matplotlib.pyplot as plt


np.random.seed(42)
sample_size = 1000

# Inter-arrival time: exponential distribution with mean 5 minutes.
inter_arrival = np.random.exponential(scale=5.0, size=sample_size)

# Service time: uniform distribution between 2 and 8 minutes.
service_times = np.random.uniform(2.0, 8.0, size=sample_size)

# Sample statistics.
sample_arr_mean = np.mean(inter_arrival)
sample_arr_std = np.std(inter_arrival, ddof=1)
sample_ser_mean = np.mean(service_times)
sample_ser_std = np.std(service_times, ddof=1)

# Theoretical statistics.
theoretical_arr_mean = 5.0
theoretical_arr_std = 5.0
theoretical_ser_mean = (2.0 + 8.0) / 2
theoretical_ser_std = (8.0 - 2.0) / np.sqrt(12)

print("--- Inter-Arrival Time: Exponential(mean=5 minutes) ---")
print(f"Sample mean       : {sample_arr_mean:.4f} minutes")
print(f"Theoretical mean   : {theoretical_arr_mean:.4f} minutes")
print(f"Sample std. dev.  : {sample_arr_std:.4f} minutes")
print(f"Theoretical std. dev.: {theoretical_arr_std:.4f} minutes")

print("\n--- Service Time: Uniform(2, 8 minutes) ---")
print(f"Sample mean       : {sample_ser_mean:.4f} minutes")
print(f"Theoretical mean   : {theoretical_ser_mean:.4f} minutes")
print(f"Sample std. dev.  : {sample_ser_std:.4f} minutes")
print(f"Theoretical std. dev.: {theoretical_ser_std:.4f} minutes")

# Plot the two required histograms.
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].hist(inter_arrival, bins=25, density=True, color="skyblue", edgecolor="black")
axes[0].axvline(sample_arr_mean, color="red", linestyle="--",
                label=f"Sample mean = {sample_arr_mean:.2f}")
axes[0].axvline(theoretical_arr_mean, color="navy", linestyle=":",
                label="Theoretical mean = 5.00")
axes[0].set_title("Inter-Arrival Times")
axes[0].set_xlabel("Time (minutes)")
axes[0].set_ylabel("Probability density")
axes[0].legend()

axes[1].hist(service_times, bins=20, density=True, color="lightgreen", edgecolor="black")
axes[1].axvline(sample_ser_mean, color="red", linestyle="--",
                label=f"Sample mean = {sample_ser_mean:.2f}")
axes[1].axvline(theoretical_ser_mean, color="darkgreen", linestyle=":",
                label="Theoretical mean = 5.00")
axes[1].set_title("Service Times")
axes[1].set_xlabel("Time (minutes)")
axes[1].set_ylabel("Probability density")
axes[1].legend()

fig.suptitle("Arrival and Service Time Simulation", fontsize=15)
fig.tight_layout()
output_file = "arrival_service_histograms.png"
fig.savefig(output_file, dpi=150)
print(f"\nGraph successfully saved to '{output_file}'")
plt.show()
