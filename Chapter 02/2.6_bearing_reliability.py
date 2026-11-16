from pathlib import Path
import random

import matplotlib.pyplot as plt

# Step 1: Define the probability tables and costs.
random.seed(42)

bearing_lives = [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]
bearing_probabilities = [10, 14, 24, 14, 12, 10, 6, 5, 3, 2]
delay_times = [4, 6, 8]
delay_probabilities = [3, 6, 1]

simulation_hours = 30_000
number_of_bearings = 3
bearing_cost = 20
repairman_cost_per_hour = 25
downtime_cost_per_minute = 5

# Manual option: uncomment these lines and add values from the question.
# manual_bearing_lives = [1200, 1500, 1100, 1400, 1300, 1600]
# manual_delays = [6, 4, 8, 6]
manual_bearing_lives = None
manual_delays = None
manual_life_index = 0
manual_delay_index = 0


def get_bearing_life():
    """Generate one bearing life from the probability distribution."""
    global manual_life_index
    if manual_bearing_lives is not None:
        if manual_life_index >= len(manual_bearing_lives):
            raise ValueError("Add more manual bearing-life values.")
        life = manual_bearing_lives[manual_life_index]
        manual_life_index += 1
        return life
    return random.choices(bearing_lives, weights=bearing_probabilities)[0]


def get_delay_time():
    """Generate one repairman delay from the probability distribution."""
    global manual_delay_index
    if manual_delays is not None:
        if manual_delay_index >= len(manual_delays):
            raise ValueError("Add more manual delay values.")
        delay = manual_delays[manual_delay_index]
        manual_delay_index += 1
        return delay
    return random.choices(delay_times, weights=delay_probabilities)[0]


def repair_minutes(number_replaced):
    """Return the machine repair time for one, two, or three bearings."""
    return {1: 20, 2: 30, 3: 40}[number_replaced]


def calculate_cost(events):
    """Calculate bearing, downtime, and repairman costs for failure events."""
    replaced = sum(number for _, number, _ in events)
    delay_minutes = sum(delay for _, _, delay in events)
    repair_minutes_total = sum(repair_minutes(number) for _, number, _ in events)

    bearing_expense = replaced * bearing_cost
    downtime_expense = (delay_minutes + repair_minutes_total) * downtime_cost_per_minute
    repairman_expense = repair_minutes_total / 60 * repairman_cost_per_hour
    return bearing_expense + downtime_expense + repairman_expense


def simulate_present_policy():
    """Replace only the failed bearing, as in the current policy."""
    failure_events = []
    all_lives = []

    for _ in range(number_of_bearings):
        clock = 0
        while clock < simulation_hours:
            life = get_bearing_life()
            clock += life
            all_lives.append(life)
            if clock <= simulation_hours:
                failure_events.append((clock, 1, get_delay_time()))

    return failure_events, all_lives


def simulate_proposed_policy():
    """Replace all three bearings when the first bearing fails."""
    failure_events = []
    first_failure_lives = []
    clock = 0

    while clock < simulation_hours:
        lives = [get_bearing_life() for _ in range(number_of_bearings)]
        first_failure = min(lives)
        clock += first_failure
        first_failure_lives.append(first_failure)
        if clock <= simulation_hours:
            failure_events.append((clock, number_of_bearings, get_delay_time()))

    return failure_events, first_failure_lives


# Step 2: Simulate both maintenance policies.
present_events, present_lives = simulate_present_policy()
proposed_events, proposed_lives = simulate_proposed_policy()
present_cost = calculate_cost(present_events)
proposed_cost = calculate_cost(proposed_events)

print("Simulation Hours          =", simulation_hours)
print("\nPresent Policy: replace one failed bearing")
print("Bearing replacements      =", sum(number for _, number, _ in present_events))
print("Failure events             =", len(present_events))
print("Maintenance cost           =", round(present_cost, 2), "Rs.")

print("\nProposed Policy: replace all three bearings")
print("Bearing replacements      =", sum(number for _, number, _ in proposed_events))
print("Failure events             =", len(proposed_events))
print("Maintenance cost           =", round(proposed_cost, 2), "Rs.")
print("\nEstimated saving            =", round(present_cost - proposed_cost, 2), "Rs.")

# Step 3: Plot life distributions and policy costs.
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
axes[0].hist(
    present_lives,
    bins=range(950, 2001, 100),
    color="cornflowerblue",
    edgecolor="black",
)
axes[0].set_title("Bearing Life Distribution")
axes[0].set_xlabel("Bearing life (hours)")
axes[0].set_ylabel("Number of generated lives")

bars = axes[1].bar(
    ["Present policy", "Proposed policy"],
    [present_cost, proposed_cost],
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
