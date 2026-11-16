from pathlib import Path
import random

import matplotlib.pyplot as plt

# Step 1: Probability tables for bearing life and mechanic delay.
random.seed(42)

bearing_lives = [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]
bearing_probabilities = [10, 14, 24, 14, 12, 10, 6, 5, 3, 2]
delay_times = [4, 6, 8]
delay_probabilities = [3, 6, 1]

operating_hours = 20_000
bearing_cost = 20
replacement_minutes = 20
delay_cost_per_minute = 5
mechanic_cost_per_hour = 25

# Manual option: uncomment these lines and add values from the question.
# manual_bearing_lives = [1500, 1200, 1800, 1100, 1600, 1400]
# manual_delays = [4, 6, 8, 6]
manual_bearing_lives = None
manual_delays = None
manual_life_index = 0
manual_delay_index = 0


def get_bearing_life():
    """Return one bearing life using the probability table."""
    global manual_life_index
    if manual_bearing_lives is not None:
        if manual_life_index == len(manual_bearing_lives):
            raise ValueError("Add more manual bearing-life values.")
        life = manual_bearing_lives[manual_life_index]
        manual_life_index += 1
        return life
    return random.choices(bearing_lives, weights=bearing_probabilities)[0]


def get_delay_time():
    """Return one mechanic delay using the probability table."""
    global manual_delay_index
    if manual_delays is not None:
        if manual_delay_index == len(manual_delays):
            raise ValueError("Add more manual delay values.")
        delay = manual_delays[manual_delay_index]
        manual_delay_index += 1
        return delay
    return random.choices(delay_times, weights=delay_probabilities)[0]


def get_failure_history():
    """Simulate three separate bearings until each reaches operating_hours."""
    histories = [[], [], []]

    for bearing_number in range(3):
        elapsed = 0
        while elapsed < operating_hours:
            life = get_bearing_life()
            histories[bearing_number].append(life)
            elapsed += life

    return histories


def count_simultaneous_failures(histories):
    """Count failures occurring together in the three bearing histories."""
    two_bearings_down = 0
    three_bearings_down = 0

    common_events = min(len(history) for history in histories)
    for event in range(common_events):
        lives = [
            histories[0][event],
            histories[1][event],
            histories[2][event],
        ]
        different_lives = len(set(lives))
        if different_lives == 1:
            three_bearings_down += 1
        elif different_lives == 2:
            two_bearings_down += 1

    return two_bearings_down, three_bearings_down


def calculate_old_cost(histories, two_bearings_down, three_bearings_down):
    """Calculate cost when each bearing is replaced separately."""
    total_bearings = sum(len(history) for history in histories)
    mechanic_calls = total_bearings - two_bearings_down - 2 * three_bearings_down
    total_delay = sum(get_delay_time() for _ in range(mechanic_calls))

    repair_minutes = (
        total_bearings * replacement_minutes
        - two_bearings_down * 10
        - three_bearings_down * 20
    )
    return (
        total_bearings * bearing_cost
        + total_delay * delay_cost_per_minute
        + repair_minutes / 60 * mechanic_cost_per_hour
    )


# Step 2: Simulate the current maintenance method.
histories = get_failure_history()
two_down, three_down = count_simultaneous_failures(histories)
old_cost = calculate_old_cost(histories, two_down, three_down)

# Step 3: Simulate replacing all three bearings when the first one fails.
grouped_lives = []
grouped_delays = []
elapsed = 0
while elapsed < operating_hours:
    first_failure = min(get_bearing_life(), get_bearing_life(), get_bearing_life())
    grouped_lives.append(first_failure)
    grouped_delays.append(get_delay_time())
    elapsed += first_failure

new_cost = (
    len(grouped_lives) * bearing_cost
    + sum(grouped_delays) * delay_cost_per_minute
    + len(grouped_lives) * 40 / 60 * mechanic_cost_per_hour
)

all_lives = histories[0] + histories[1] + histories[2]
print("Individual replacement cost =", round(old_cost, 2), "Rs.")
print("Group replacement cost      =", round(new_cost, 2), "Rs.")
print("Estimated saving             =", round(old_cost - new_cost, 2), "Rs.")
print("Individual bearing failures  =", len(all_lives))
print("Grouped replacement events  =", len(grouped_lives))
print("Two bearings down together   =", two_down)
print("Three bearings down together =", three_down)

# Step 4: Draw graphs.
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
axes[0].hist(all_lives, bins=10, color="cornflowerblue", edgecolor="black")
axes[0].set_title("Bearing Life Distribution")
axes[0].set_xlabel("Bearing life (hours)")
axes[0].set_ylabel("Number of failures")

bars = axes[1].bar(
    ["Individual\nreplacement", "Group\nreplacement"],
    [old_cost, new_cost],
    color=["indianred", "seagreen"],
)
axes[1].set_title("Maintenance Cost Comparison")
axes[1].set_ylabel("Cost (Rs.)")
axes[1].bar_label(bars, fmt="%.2f", padding=3)

fig.suptitle("Bearing Reliability Simulation", fontsize=16)
fig.tight_layout()
output_file = Path(__file__).with_name("2.6_bearing_reliability.png")
fig.savefig(output_file, dpi=150)
print(f"Graph saved to '{output_file}'")
plt.show()
