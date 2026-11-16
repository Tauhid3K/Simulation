from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Step 1: Define bearing life and mechanic-delay distributions.
rng = np.random.default_rng(42)
life_values = np.arange(1000, 2000, 100)
life_probabilities = np.array([0.10, 0.14, 0.24, 0.14, 0.12, 0.10, 0.06, 0.05, 0.03, 0.02])
delay_values = np.array([4, 6, 8])
delay_probabilities = np.array([0.3, 0.6, 0.1])
replacement_time = 20
replacement_cost = 20
delay_cost_per_minute = 5
mechanic_cost_per_hour = 25
operating_time = 20_000

# Manual option: uncomment these lines to use question-provided values.
# manual_bearing_lives = [1800, 1200, 1600, 1300, 1100, 1000]
# manual_mechanic_delays = [4, 6, 8, 6]
manual_bearing_lives = None
manual_mechanic_delays = None
manual_life_index = 0
manual_delay_index = 0


def simulate_life() -> int:
    global manual_life_index
    if manual_bearing_lives is not None:
        if manual_life_index >= len(manual_bearing_lives):
            raise ValueError("Add more manual bearing-life values for the simulation.")
        life = manual_bearing_lives[manual_life_index]
        manual_life_index += 1
        return int(life)
    return int(rng.choice(life_values, p=life_probabilities))


def simulate_delay() -> int:
    global manual_delay_index
    if manual_mechanic_delays is not None:
        if manual_delay_index >= len(manual_mechanic_delays):
            raise ValueError("Add more manual mechanic-delay values for the simulation.")
        delay_value = manual_mechanic_delays[manual_delay_index]
        manual_delay_index += 1
        return int(delay_value)
    return int(rng.choice(delay_values, p=delay_probabilities))


def simulate_individual_bearings() -> tuple[list[int], int, int]:
    bearing_lives = [[], [], []]
    elapsed = [0, 0, 0]
    while min(elapsed) < operating_time:
        for index in range(3):
            if elapsed[index] < operating_time:
                life = simulate_life()
                bearing_lives[index].append(life)
                elapsed[index] += life

    two_down = 0
    three_down = 0
    for lives in zip(*bearing_lives):
        equal_count = len(set(lives))
        if equal_count == 1:
            three_down += 1
        elif equal_count == 2:
            two_down += 1

    return [life for bearing in bearing_lives for life in bearing], two_down, three_down


def calculate_cost(number_of_bearings: int, two_down: int, three_down: int) -> float:
    mechanic_calls = number_of_bearings - two_down - 2 * three_down
    delay_minutes = sum(simulate_delay() for _ in range(max(mechanic_calls, 0)))
    repair_minutes = number_of_bearings * replacement_time - 10 * two_down - 20 * three_down
    return (
        number_of_bearings * replacement_cost
        + delay_minutes * delay_cost_per_minute
        + repair_minutes / 60 * mechanic_cost_per_hour
    )


individual_lives, two_down, three_down = simulate_individual_bearings()
old_cost = calculate_cost(len(individual_lives), two_down, three_down)

grouped_lives = []
grouped_delays = []
elapsed = 0

while elapsed < operating_time:
    grouped_lives.append(min(simulate_life(), simulate_life(), simulate_life()))
    grouped_delays.append(simulate_delay())
    elapsed += grouped_lives[-1]

new_cost = (
    len(grouped_lives) * replacement_cost
    + sum(grouped_delays) * delay_cost_per_minute
    + len(grouped_lives) * 40 / 60 * mechanic_cost_per_hour
)

print("Individual replacement cost =", round(old_cost, 2), "Rs.")
print("Group replacement cost      =", round(new_cost, 2), "Rs.")
print("Estimated saving             =", round(old_cost - new_cost, 2), "Rs.")
print("Individual bearing failures  =", len(individual_lives))
print("Grouped replacement events  =", len(grouped_lives))
print("Two bearings down together   =", two_down)
print("Three bearings down together =", three_down)

# Step 2: Compare bearing-life distributions and replacement costs.
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
axes[0].hist(individual_lives, bins=np.arange(950, 2051, 100), color="cornflowerblue", edgecolor="black")
axes[0].set_title("Individual Bearing Lifetimes")
axes[0].set_xlabel("Life (hours)")
axes[0].set_ylabel("Frequency")

bars = axes[1].bar(["Individual", "Grouped"], [old_cost, new_cost], color=["indianred", "seagreen"])
axes[1].set_title("Replacement Cost Comparison")
axes[1].set_ylabel("Cost (Rs.)")
axes[1].bar_label(bars, fmt="%.2f", padding=3)

fig.suptitle("Bearing Reliability Simulation", fontsize=16)
fig.tight_layout()
output_file = Path(__file__).with_name("2.6_bearing_reliability.png")
fig.savefig(output_file, dpi=150)
print(f"Graph saved to '{output_file}'")
plt.show()
