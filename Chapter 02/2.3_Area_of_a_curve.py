
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Step 1: Rectangle Area
A = 3 * 140

# Step 2: Generate Random Points
N = 1000

x = 2 + np.random.rand(N) * 3
y = np.random.rand(N) * 140

# To use manually supplied random coordinates, uncomment these lines and
# replace the example values with x and y values in the rectangle.
# manual_x = [2.2, 3.1, 4.0, 4.8]
# manual_y = [10.0, 35.0, 80.0, 120.0]
# x = np.array(manual_x)
# y = np.array(manual_y)
# N = len(x)

# Step 3: Check Inside or Outside
inside = y < x**3        #bolean akare value store korbe 

# Step 4: Count Inside Points
M = 0

for i in range(N):
    if inside[i]:
        M = M + 1

# Step 5: Calculate Integral
I = (M / N) * A

print("Total Points =", N)
print("Inside Points =", M)
print("Rectangle Area =", A)
print("Estimated Integral =", round(I, 2))

# Step 6: Draw Graph
fig, ax = plt.subplots(figsize=(8, 7))

ax.scatter(x[inside], y[inside], color="green", s=12, alpha=0.65, label="Inside")
ax.scatter(x[~inside], y[~inside], color="red", s=12, alpha=0.65, label="Outside")

# Draw Boundary
xx = np.linspace(2, 5, 100)
yy = xx**3

ax.plot(xx, yy, color="blue", linewidth=2, label="y = x³")
ax.fill_between(xx, 0, yy, color="green", alpha=0.12)

ax.set_xlim(2, 5)
ax.set_ylim(0, 140)

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_title(f"Monte Carlo Integration (Estimated area: {I:.2f})")
ax.legend()
ax.grid(alpha=0.3)

fig.tight_layout()
output_file = Path(__file__).with_name("2.3_curve_area.png")
fig.savefig(output_file, dpi=150)
print(f"Graph saved to '{output_file}'")
plt.show()
