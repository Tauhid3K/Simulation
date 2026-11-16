from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Step 1: Define the equipment and maintenance rules.
simulation_hours = 6_000
number_of_tubes = 4
tube_cost = 100
downtime_cost_per_hour = 200
downtime_hours = 1
rng = np.random.default_rng(42)

# To reproduce the textbook example, uncomment these digits.
# manual_random_digits = [8, 2, 6, 3, 1, 0, 8, 9, 2, 8, 3, 7, 4, 8, 5, 6, 0, 4, 9]
manual_random_digits = None

# Manual option for complete tube-life values:
# manual_tube_lives = [1800, 1200, 1600, 1300, 1100, 1000, 1800, 1900]
# manual_random_digits = [(life - 1000) // 100 for life in manual_tube_lives]


def next_tube_life() -> int:
    """Generate a tube life uniformly from 1000 through 1900 hours."""
    if manual_random_digits is not None:
        if not manual_random_digits:
            raise ValueError("Add more manual random digits for the simulation.")
        return 1_000 + 100 * manual_random_digits.pop(0)
    return int(rng.integers(10, size=1)[0]) * 100 + 1_000


# Step 2: Start with four new tubes at time zero.
remaining_lives = np.array([next_tube_life() for _ in range(number_of_tubes)], dtype=int)
clock = 0
failure_times = []
replacement_counts = []
maintenance_costs = []
total_cost = 0

# Step 3: Advance the clock to each failure and replace all tubes that fail.
while True:
    time_to_failure = int(remaining_lives.min())
    if clock + time_to_failure > simulation_hours:
        break

    clock += time_to_failure
    remaining_lives -= time_to_failure
    failed_tubes = np.flatnonzero(remaining_lives == 0)
    replacements = len(failed_tubes)
    event_cost = replacements * tube_cost + downtime_hours * downtime_cost_per_hour

    remaining_lives[failed_tubes] = [next_tube_life() for _ in failed_tubes]
    total_cost += event_cost
    failure_times.append(clock)
    replacement_counts.append(replacements)
    maintenance_costs.append(total_cost)

total_failures = len(failure_times)
total_replacements = sum(replacement_counts)

print("Simulation Hours       =", simulation_hours)
print("System Failure Events  =", total_failures)
print("Tubes Replaced         =", total_replacements)
print("Tube Replacement Cost  =", total_replacements * tube_cost, "Rs.")
print("Downtime Cost           =", total_failures * downtime_cost_per_hour, "Rs.")
print("Total Maintenance Cost  =", total_cost, "Rs.")

# Step 4: Plot failure events and cumulative maintenance cost.
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

axes[0].step(failure_times, replacement_counts, where="post", color="darkorange", linewidth=1.5)
axes[0].scatter(failure_times, replacement_counts, color="darkorange", zorder=3)
axes[0].set_title("Tube Failure Events")
axes[0].set_xlabel("Operating time (hours)")
axes[0].set_ylabel("Tubes replaced")
axes[0].set_yticks(range(1, max(replacement_counts, default=1) + 1))
axes[0].grid(alpha=0.3)

axes[1].step(failure_times, maintenance_costs, where="post", color="seagreen", linewidth=2)
axes[1].set_title(f"Cumulative Maintenance Cost: Rs. {total_cost}")
axes[1].set_xlabel("Operating time (hours)")
axes[1].set_ylabel("Cost (Rs.)")
axes[1].grid(alpha=0.3)

fig.suptitle("Four-Tube Equipment Maintenance Simulation", fontsize=16)
fig.tight_layout()
output_file = Path(__file__).with_name("2.9_equipment_tubes.png")
fig.savefig(output_file, dpi=150)
print(f"Graph saved to '{output_file}'")
plt.show()
