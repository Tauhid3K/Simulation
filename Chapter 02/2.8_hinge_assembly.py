from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Step 1: Generate dimensions for each hinge assembly.
rng = np.random.default_rng(42)
number_of_assemblies = 10_000
assembly_parts = rng.uniform(
    low=[1.95, 1.95, 29.95, 34.00],
    high=[2.05, 2.05, 30.95, 35.00],
    size=(number_of_assemblies, 4),
)

# Manual option: uncomment these lines and enter A, B, C, and D values.
# manual_parts = [
#     [2.00, 2.01, 30.20, 34.50],
#     [1.98, 2.03, 30.10, 34.00],
# ]
# assembly_parts = np.array(manual_parts, dtype=float)
# number_of_assemblies = len(assembly_parts)

part_a, part_b, part_c, part_d = assembly_parts.T
sum_abc = part_a + part_b + part_c
clearance = part_d - sum_abc
successful = clearance >= 0
success_count = int(successful.sum())
success_rate = success_count / number_of_assemblies * 100

print("Total Assemblies =", number_of_assemblies)
print("Successful       =", success_count)
print("Unsuccessful     =", number_of_assemblies - success_count)
print("Success Rate     =", round(success_rate, 2), "%")
print("Average Clearance =", round(clearance.mean(), 4))

# Step 2: Plot clearance and success/failure results.
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
axes[0].hist(clearance, bins=30, color="cornflowerblue", edgecolor="black")
axes[0].axvline(0, color="red", linestyle="--", label="Required clearance")
axes[0].set_title("Hinge Assembly Clearance")
axes[0].set_xlabel("D - (A + B + C)")
axes[0].set_ylabel("Number of assemblies")
axes[0].legend()

bars = axes[1].bar(["Successful", "Failed"], [success_count, number_of_assemblies - success_count],
                   color=["seagreen", "indianred"])
axes[1].set_title("Assembly Reliability")
axes[1].set_ylabel("Number of assemblies")
axes[1].bar_label(bars)

fig.suptitle("Hinge Assembly Simulation", fontsize=16)
fig.tight_layout()
output_file = Path(__file__).with_name("2.8_hinge_assembly.png")
fig.savefig(output_file, dpi=150)
print(f"Graph saved to '{output_file}'")
plt.show()
