from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Step 1: Set the random walk parameters.
rng = np.random.default_rng(42)
number_of_steps = 100
directions = np.array(["F", "L", "R", "B"])
probabilities = np.array([0.5, 0.2, 0.2, 0.1])

# Step 2: Generate steps using the given direction probabilities.
walk_directions = rng.choice(directions, size=number_of_steps, p=probabilities)

# Manual option: uncomment these lines and enter the question's directions.
# manual_directions = ["F", "R", "F", "L", "B", "R"]
# walk_directions = np.array(manual_directions)
# number_of_steps = len(walk_directions)

movement = {
    "F": (0, 1),
    "L": (-1, 0),
    "R": (1, 0),
    "B": (0, -1),
}
steps = np.array([movement[direction] for direction in walk_directions])
locations = np.vstack(([0, 0], np.cumsum(steps, axis=0)))

print("Number of Steps =", number_of_steps)
final_x, final_y = locations[-1]
print("Final x =", final_x)
print("Final y =", final_y)
print("Distance from Origin =", round(np.linalg.norm(locations[-1]), 2))
print("Directions =", "".join(walk_directions))

# Step 3: Plot the path and its distance from the origin.
distance = np.linalg.norm(locations, axis=1)
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

axes[0].plot(locations[:, 0], locations[:, 1], color="purple", linewidth=1.5)
axes[0].scatter(*locations[0], color="green", s=70, label="Start")
axes[0].scatter(*locations[-1], color="red", s=70, label="End")
axes[0].set_title("Random Walk Path")
axes[0].set_xlabel("X position")
axes[0].set_ylabel("Y position")
axes[0].axis("equal")
axes[0].grid(alpha=0.3)
axes[0].legend()

axes[1].plot(np.arange(number_of_steps + 1), distance, color="teal")
axes[1].set_title("Distance from Origin")
axes[1].set_xlabel("Step")
axes[1].set_ylabel("Distance")
axes[1].grid(alpha=0.3)

fig.suptitle("Monte Carlo Random Walk", fontsize=16)
fig.tight_layout()
output_file = Path(__file__).with_name("2.5_random_walk.png")
fig.savefig(output_file, dpi=150)
print(f"Graph saved to '{output_file}'")
plt.show()
