from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Step 1: Define the target rectangle and normal-distribution spread.
rng = np.random.default_rng(42)
length = 1_000
height = 600
number_of_strikes = 10_000
coordinates = rng.normal(0, [length / 2, height / 2], size=(number_of_strikes, 2))

# Manual option: uncomment these lines and enter the question's coordinates.
# manual_x = [-400, 0, 250, 600]
# manual_y = [-200, 100, 350, 500]
# coordinates = np.column_stack((manual_x, manual_y))
# number_of_strikes = len(coordinates)

inside = (
    (coordinates[:, 0] >= -length / 2)
    & (coordinates[:, 0] <= length / 2)
    & (coordinates[:, 1] >= -height / 2)
    & (coordinates[:, 1] <= height / 2)
)
hit_count = int(inside.sum())
accuracy = hit_count / number_of_strikes * 100

print("Total Strikes =", number_of_strikes)
print("Hits          =", hit_count)
print("Misses        =", number_of_strikes - hit_count)
print("Accuracy      =", round(accuracy, 2), "%")

# Step 2: Plot strikes and the target rectangle.
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(coordinates[~inside, 0], coordinates[~inside, 1], color="blue", s=4, alpha=0.2, label="Miss")
ax.scatter(coordinates[inside, 0], coordinates[inside, 1], color="green", s=4, alpha=0.2, label="Hit")
rectangle_x = [-length / 2, length / 2, length / 2, -length / 2, -length / 2]
rectangle_y = [-height / 2, -height / 2, height / 2, height / 2, -height / 2]
ax.plot(rectangle_x, rectangle_y, color="red", linewidth=2, label="Target area")
ax.set_xlabel("X position")
ax.set_ylabel("Y position")
ax.set_title(f"Strike Simulation (Accuracy: {accuracy:.2f}%)")
ax.set_aspect("equal")
ax.grid(alpha=0.3)
ax.legend()

fig.tight_layout()
output_file = Path(__file__).with_name("2.7_number_of_strike.png")
fig.savefig(output_file, dpi=150)
print(f"Graph saved to '{output_file}'")
plt.show()
