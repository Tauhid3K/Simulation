
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Step 1: Total Games
N = 1000

# Step 2: Initialize Variables
total_flips = 0     #সব Game-এ মোট কতবার Toss হয়েছে
total_return = 0    #মোট কত টাকা পুরস্কার পেয়েছি

win = 0
lose = 0
flips_per_game = []

# Step 3: Simulate Games
for game in range(N):

    heads = 0
    tails = 0
    flips = 0

    while abs(heads - tails) < 3:

        r = np.random.rand()

        if r < 0.5:
            heads = heads + 1
        else:
            tails = tails + 1

        flips = flips + 1

    # Step 4: Count Total Flips
    total_flips = total_flips + flips
    flips_per_game.append(flips)

    # Step 5: Calculate Win or Lose
    if flips < 8:
        total_return = total_return + 8
        win = win + 1

    elif flips > 8:
        lose = lose + 1

# To use manually supplied results instead of simulating games, uncomment
# this block and replace the example flip counts.
# flips_per_game = [3, 5, 7, 9, 11, 13]
# N = len(flips_per_game)
# total_flips = sum(flips_per_game)
# total_return = sum(8 for flips in flips_per_game if flips < 8)
# win = sum(flips < 8 for flips in flips_per_game)
# lose = sum(flips > 8 for flips in flips_per_game)

# Step 6: Calculate Cost and Profit
total_cost = total_flips
profit = total_return - total_cost

average_flips = total_flips / N

# Step 7: Display Result
print("Total Games =", N)
print("Total Flips =", total_flips)
print("Total Cost =", total_cost, "Rs.")
print("Total Return =", total_return, "Rs.")
print("Winning Games =", win)
print("Losing Games =", lose)
print("Average Flips =", round(average_flips, 2))
print("Total Profit/Loss =", profit, "Rs.")

# Step 8: Plot game results
flips_per_game = np.array(flips_per_game)

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

axes[0].hist(flips_per_game, bins=np.arange(flips_per_game.min() - 0.5, flips_per_game.max() + 1.5),
             color="cornflowerblue", edgecolor="black")
axes[0].axvline(8, color="red", linestyle="--", label="8 flips")
axes[0].set_title("Distribution of Flips per Game")
axes[0].set_xlabel("Flips")
axes[0].set_ylabel("Number of games")
axes[0].legend()

outcomes = [win, lose, N - win - lose]
bars = axes[1].bar(["Win\n(< 8)", "Lose\n(> 8)", "Break-even\n(= 8)"], outcomes,
                   color=["seagreen", "indianred", "darkorange"])
axes[1].set_title("Game Outcomes")
axes[1].set_ylabel("Number of games")
axes[1].bar_label(bars)

fig.suptitle("Heads/Tails Stopping Game Simulation", fontsize=16)
fig.tight_layout()
output_file = Path(__file__).with_name("2.2_heads_tails_analysis.png")
fig.savefig(output_file, dpi=150)
print(f"Graph saved to '{output_file}'")
plt.show()
