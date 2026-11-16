from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def estimate_pi(number_of_points: int, rng: np.random.Generator) -> tuple[float, int]:
    """Estimate pi using random points in a unit square and quarter-circle."""
    points = rng.uniform(0, 1, size=(number_of_points, 2))

    # To use manually supplied random coordinates, uncomment these lines.
    # manual_x = [0.2, 0.7, 0.9, 0.4]
    # manual_y = [0.3, 0.8, 0.1, 0.6]
    # points = np.column_stack((manual_x, manual_y))
    # number_of_points = len(points)

    inside = np.sum(points[:, 0] ** 2 + points[:, 1] ** 2 <= 1)
    return 4 * inside / number_of_points, int(inside)


sample_sizes = np.array([100, 1_000, 10_000, 100_000])
rng = np.random.default_rng(42)
estimates = []

print("Monte Carlo Estimation of pi")
print("-" * 45)
for sample_size in sample_sizes:
    estimate, inside_count = estimate_pi(int(sample_size), rng)
    estimates.append(estimate)
    print(
        f"Points: {sample_size:>6} | "
        f"Inside quarter-circle: {inside_count:>6} | "
        f"Estimated pi: {estimate:.6f}"
    )

estimates = np.array(estimates)
output_file = Path(__file__).with_name("pi_estimation.png")

# Generate points for a visual example of the square and quarter-circle.
display_points = rng.uniform(0, 1, size=(10_000, 2))
display_inside = display_points[:, 0] ** 2 + display_points[:, 1] ** 2 <= 1
theta = np.linspace(0, np.pi / 2, 200)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

axes[0].scatter(display_points[~display_inside, 0], display_points[~display_inside, 1],
                color="red", s=5, alpha=0.35, label="Outside quarter-circle")
axes[0].scatter(display_points[display_inside, 0], display_points[display_inside, 1],
                color="green", s=5, alpha=0.35, label="Inside quarter-circle")
axes[0].plot(np.cos(theta), np.sin(theta), color="blue", linewidth=2, label="Quarter-circle")
axes[0].plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], color="black", linewidth=1)
axes[0].set_xlim(0, 1)
axes[0].set_ylim(0, 1)
axes[0].set_aspect("equal")
axes[0].set_xlabel("x")
axes[0].set_ylabel("y")
axes[0].set_title("Random Points in a Square")
axes[0].grid(alpha=0.3)
axes[0].legend(loc="upper right")

ax = axes[1]
ax.plot(sample_sizes, estimates, marker="o", linewidth=2, label="Estimated pi")
ax.axhline(np.pi, color="red", linestyle="--", label=f"Actual pi: {np.pi:.6f}")
ax.set_xscale("log")
ax.set_xlabel("Number of generated points")
ax.set_ylabel("Estimated value of pi")
ax.set_title("Monte Carlo Estimation of pi")
ax.set_xticks(sample_sizes)
ax.set_xticklabels([str(size) for size in sample_sizes])
ax.set_ylim(2.5, 3.8)
ax.grid(True, alpha=0.3)
ax.legend()

for sample_size, estimate in zip(sample_sizes, estimates):
    ax.annotate(f"{estimate:.4f}", (sample_size, estimate), xytext=(0, 8),
                textcoords="offset points", ha="center")

fig.tight_layout()
fig.savefig(output_file, dpi=150)
print(f"\nGraph saved to '{output_file}'")
plt.show()