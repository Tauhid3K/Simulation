from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Step 1: Generate random points in a unit square.
rng = np.random.default_rng(42)
number_of_points = 10_000
points = rng.uniform(0, 1, size=(number_of_points, 2))

# Manual option: uncomment these lines and enter the question's coordinates.
# manual_x = [0.20, 0.70, 0.90, 0.40]
# manual_y = [0.30, 0.80, 0.10, 0.60]
# points = np.column_stack((manual_x, manual_y))
# number_of_points = len(points)

inside = np.sum(points**2, axis=1) <= 1
inside_count = int(inside.sum())

# Step 2: Estimate pi from the quarter-circle proportion.
estimated_pi = 4 * inside_count / number_of_points
error = abs(np.pi - estimated_pi)

print("Total Points   =", number_of_points)
print("Inside Points  =", inside_count)
print("Estimated pi   =", round(estimated_pi, 6))
print("Actual pi      =", round(np.pi, 6))
print("Absolute Error =", round(error, 6))

# Step 3: Draw the square, quarter-circle, and sampled points.
theta = np.linspace(0, np.pi / 2, 200)
fig, ax = plt.subplots(figsize=(8, 8))
ax.scatter(points[~inside, 0], points[~inside, 1], color="blue", s=5, alpha=0.25, label="Outside")
ax.scatter(points[inside, 0], points[inside, 1], color="green", s=5, alpha=0.25, label="Inside")
ax.plot(np.cos(theta), np.sin(theta), color="red", linewidth=2, label="Quarter-circle")
ax.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], color="black", linewidth=1)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect("equal")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title(f"Value of pi by Monte Carlo: {estimated_pi:.4f}")
ax.legend()
ax.grid(alpha=0.3)

fig.tight_layout()
output_file = Path(__file__).with_name("2.4_value_of_pi.png")
fig.savefig(output_file, dpi=150)
print(f"Graph saved to '{output_file}'")
plt.show()
