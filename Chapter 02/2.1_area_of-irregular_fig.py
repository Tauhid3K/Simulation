import matplotlib.pyplot as plt
import numpy as np
from matplotlib.path import Path
from pathlib import Path as FilePath

# The enclosing square has the same dimensions as Example 2.1.
square_side = 9.0
square_area = square_side**2

# Vertices approximate the irregular outline shown in Fig. 2.1.
boundary = np.array([
    (1.5, 1.2), (3.3, 1.2), (3.3, 2.2), (4.8, 2.2),
    (4.8, 1.2), (6.6, 1.2), (6.6, 3.0), (7.5, 3.3),
    (7.8, 4.2), (7.7, 5.2), (7.2, 6.0), (6.2, 6.5),
    (5.4, 6.6), (5.0, 7.0), (5.0, 7.8), (4.6, 8.2),
    (3.7, 8.1), (3.3, 7.6), (3.3, 6.9), (2.0, 6.9),
    (2.0, 5.7), (3.3, 4.8), (2.0, 3.9), (2.0, 1.2),
])

# Calibrate the reconstructed outline to the textbook's stated ratio,
# F/A = 0.3126, because the scanned figure does not provide coordinates.
textbook_area = 0.3126 * square_area
polygon_area = 0.5 * abs(
    np.dot(boundary[:, 0], np.roll(boundary[:, 1], -1))
    - np.dot(boundary[:, 1], np.roll(boundary[:, 0], -1))
)
centroid = boundary.mean(axis=0)
boundary = centroid + (boundary - centroid) * np.sqrt(textbook_area / polygon_area)

# Use a fixed seed so the result can be reproduced.
rng = np.random.default_rng(42)
number_of_points = 10_000
points = rng.uniform(0, square_side, size=(number_of_points, 2))

# To use manually supplied random coordinates, uncomment these lines and
# replace the example values with your x and y values (0 <= x,y <= 9).
# manual_x = [1.2, 4.5, 7.8, 2.4]
# manual_y = [2.1, 6.3, 5.0, 8.2]
# points = np.column_stack((manual_x, manual_y))
# number_of_points = len(points)

inside = Path(boundary).contains_points(points)
inside_points = points[inside]
inside_count = inside.sum()

# Exact area of the polygon, using the shoelace formula.
x_coordinates = boundary[:, 0]
y_coordinates = boundary[:, 1]
true_area = 0.5 * abs(
    np.dot(x_coordinates, np.roll(y_coordinates, -1))
    - np.dot(y_coordinates, np.roll(x_coordinates, -1))
)

# Monte Carlo estimate: F/A ≈ M/N.
estimated_area = square_area * inside_count / number_of_points
relative_error = abs(estimated_area - true_area) / true_area * 100

print("Total Points       =", number_of_points)
print("Inside Points      =", inside_count)
print("Square Area        =", square_area, "cm²")
print("True Polygon Area  =", round(true_area, 4), "cm²")
print("Estimated Area     =", round(estimated_area, 4), "cm²")
print("Relative Error     =", round(relative_error, 2), "%")
print("M/N                =", round(inside_count / number_of_points, 4))
print("Area Ratio         =", round(true_area / square_area, 4))

# Plot the square, sampled points, irregular boundary, and shaded region.
fig, ax = plt.subplots(figsize=(8, 8))
ax.scatter(points[~inside, 0], points[~inside, 1], color="red", s=5, alpha=0.25, label="Outside")
ax.scatter(inside_points[:, 0], inside_points[:, 1], color="green", s=5, alpha=0.25, label="Inside")

closed_boundary = np.vstack((boundary, boundary[0]))
ax.plot(closed_boundary[:, 0], closed_boundary[:, 1], color="blue", linewidth=2, label="Irregular boundary")
ax.fill(boundary[:, 0], boundary[:, 1], color="green", alpha=0.15)

ax.set_xlim(0, square_side)
ax.set_ylim(0, square_side)
ax.set_aspect("equal")
ax.set_xlabel("x (cm)")
ax.set_ylabel("y (cm)")
ax.set_title(f"Monte Carlo Area Estimation: {estimated_area:.2f} cm²")
ax.legend()
ax.grid(alpha=0.3)

fig.tight_layout()
output_file = FilePath(__file__).with_name("2.1_irregular_area.png")
fig.savefig(output_file, dpi=150)
print(f"Graph saved to '{output_file}'")
plt.show()
