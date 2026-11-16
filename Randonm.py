import numpy as np
import matplotlib.pyplot as plt

# 1. Generate 100 random numbers between 0 and 1
nums = np.random.uniform(0, 1, 100)
print("1. 100 Random Numbers:")
print(f"   Mean: {np.mean(nums):.4f}")
print(f"   Minimum: {np.min(nums):.4f}")
print(f"   Standard Deviation: {np.std(nums):.4f}")

# 2. If we generate 100 random numbers again, will the mean be exactly the same?
nums_again = np.random.uniform(0, 1, 100)
print("\n2. Generate 100 numbers again:")
print(f"   First Mean : {np.mean(nums):.4f}")
print(f"   Second Mean: {np.mean(nums_again):.4f}")
print(f"   Exactly the same? {np.mean(nums) == np.mean(nums_again)} (No, because new random values are drawn)")

# 3. What happens if we use the same random seed?
np.random.seed(42)
seed_run1 = np.random.uniform(0, 1, 100)

np.random.seed(42)
seed_run2 = np.random.uniform(0, 1, 100)

print("\n3. Using the same random seed (seed=42):")
print(f"   Run 1 Mean: {np.mean(seed_run1):.4f}")
print(f"   Run 2 Mean: {np.mean(seed_run2):.4f}")
print(f"   Exactly the same? {np.array_equal(seed_run1, seed_run2)} (Yes, seed locks the sequence)")

# 4. What will happen if we generate 10,000 instead of 100 numbers?
nums_10000 = np.random.uniform(0, 1, 10000)
print("\n4. 100 vs 10,000 Numbers:")
print(f"   100 numbers   -> Mean: {np.mean(nums):.4f}, Std Dev: {np.std(nums):.4f}, Min: {np.min(nums):.4f}")
print(f"   10,000 numbers -> Mean: {np.mean(nums_10000):.4f}, Std Dev: {np.std(nums_10000):.4f}, Min: {np.min(nums_10000):.4f}")
print("   Observation: With 10,000 numbers, the mean approaches 0.5, std dev approaches 0.2887, and min approaches 0.")

# 5. Plot the main experiments and summary statistics in one dashboard
fig, axes = plt.subplots(2, 2, figsize=(12, 9))

axes[0, 0].hist(nums, bins=15, color="steelblue", edgecolor="black")
axes[0, 0].axvline(np.mean(nums), color="red", linestyle="--", label=f"Mean: {np.mean(nums):.3f}")
axes[0, 0].set_title("100 Random Numbers")
axes[0, 0].set_xlabel("Value")
axes[0, 0].set_ylabel("Frequency")
axes[0, 0].legend()

axes[0, 1].hist(nums_again, bins=15, color="darkorange", edgecolor="black")
axes[0, 1].axvline(np.mean(nums_again), color="red", linestyle="--", label=f"Mean: {np.mean(nums_again):.3f}")
axes[0, 1].set_title("Second Independent Sample")
axes[0, 1].set_xlabel("Value")
axes[0, 1].set_ylabel("Frequency")
axes[0, 1].legend()

axes[1, 0].hist(nums, bins=15, density=True, alpha=0.65, color="steelblue", label="100 numbers")
axes[1, 0].hist(nums_10000, bins=30, density=True, alpha=0.65, color="seagreen", label="10,000 numbers")
axes[1, 0].axvline(0.5, color="black", linestyle="--", label="Theoretical mean: 0.5")
axes[1, 0].set_title("100 vs 10,000 Distribution")
axes[1, 0].set_xlabel("Value")
axes[1, 0].set_ylabel("Probability density")
axes[1, 0].legend()

summary_labels = ["100 mean", "10,000 mean", "100 std", "10,000 std"]
summary_values = [np.mean(nums), np.mean(nums_10000), np.std(nums), np.std(nums_10000)]
bars = axes[1, 1].bar(
    summary_labels,
    summary_values,
    color=["steelblue", "seagreen", "cornflowerblue", "mediumseagreen"],
)
axes[1, 1].set_title("Summary Statistics")
axes[1, 1].set_ylabel("Value")
axes[1, 1].tick_params(axis="x", rotation=25)
axes[1, 1].bar_label(bars, fmt="%.3f", padding=3)

fig.suptitle("Random Number Experiments", fontsize=16)
fig.tight_layout()
fig.savefig("random_number_analysis.png", dpi=150)
print("\nGraph successfully saved to 'random_number_analysis.png'")
plt.show()
