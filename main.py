import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.lines import Line2D

# Load the dataset
df = pd.read_excel("Assignment_Dataset.xlsx")

# Dynamic Budget Line Calculation
start_date = df["Date"].min()
df["Budget PR"] = 73.9 - ((df["Date"] - start_date).dt.days // 365) * 0.8

# Date column to datetime
df["Date"] = pd.to_datetime(df["Date"])

# 30-day moving average of PR calculation
df["30-d MA PR"] = df["PR"].rolling(window=30).mean()

# Color coding based on GHI
colors = np.select(
    [df["GHI"] < 2, (df["GHI"] >= 2) & (df["GHI"] < 4), (df["GHI"] >= 4) & (df["GHI"] < 6), df["GHI"] >= 6],
    ["navy", "lightblue", "orange", "brown"],
    default="gray"
)

# Create the plot
fig, ax = plt.subplots(figsize=(12, 6))

# Scatter plot with color coding based on PR
sc = ax.scatter(df["Date"], df["PR"], c=colors, label="Daily Irradiation", s=12, marker='$\diamond$')

# Target budget yield line (darkgreen)
ax.plot(df["Date"], df["Budget PR"], color="darkgreen", linewidth=3, label="Target Budget Yield PR")
dg_text = 'Target Budget Yield Performance Ratio'
ax.annotate(dg_text, xy=(0.5, 0.55), xycoords='axes fraction', fontsize=10, ha='center', color='darkgreen', fontweight='bold')

# 30-day moving average line (Red)
ax.plot(df["Date"], df["30-d MA PR"], color="red", linewidth=2, label="30-d Moving Average of PR")
r_text = '30-d Moving Average of Performance Ratio'
ax.annotate(r_text, xy=(0.5, 0.5), xycoords='axes fraction', fontsize=10, ha='center', color='red', fontweight='bold')

# Add labels and title
ax.set_ylabel("Performance Ratio (PR)")
ax.set_title("Performance Evolution Ratio\nFrom 2019-07 to 2022-03")

# Legend handles and labels for color-coded scatter plot
legend_handles = [
    Line2D([], [], linestyle='none', marker='$\u25C6$', markersize=5, markeredgecolor='navy', markerfacecolor='navy', label='<2'),
    Line2D([], [], linestyle='none', marker='$\u25C6$', markersize=5, markeredgecolor='lightblue', markerfacecolor='lightblue', label='2 - 4'),
    Line2D([], [], linestyle='none', marker='$\u25C6$', markersize=5, markeredgecolor='orange', markerfacecolor='orange', label='4 - 6'),
    Line2D([], [], linestyle='none', marker='$\u25C6$', markersize=5, markeredgecolor='brown', markerfacecolor='brown', label='>6'),
]

# Add the legend for color coding
legend1 = ax.legend(handles=legend_handles, title="Daily Irradiation(kWh/m2)", loc='center right', fontsize=8)
ax.add_artist(legend1)

# Set explicit X-axis tick positions
x_ticks = df["Date"][::len(df) // 11]
ax.set_xticks(x_ticks)
# Format x-axis tick labels using mdates.DateFormatter
date_formatter = mdates.DateFormatter("%b/%y")  # Format: Month/Year (e.g., Jul/19)
ax.xaxis.set_major_formatter(date_formatter)
plt.xticks()

# Y-axis ticks and labels
y_ticks = np.arange(0, 100, 10)
ax.set_yticks(y_ticks)

# Calculate and display the points above Target Budget PR
above_budget = df[df['PR'] > df['Budget PR']]
above_budget_count = len(above_budget)
total_entries = len(df)
above_budget_percent = (above_budget_count / total_entries) * 100
above_budget_text = f"Points above Target Budget PR {above_budget_count}/{total_entries} {above_budget_percent:.1f}%"
ax.annotate(above_budget_text, xy=(0.5, 0.45), xycoords='axes fraction', fontsize=10, ha='center', fontweight='bold')

# Calculate and display average PR values
average_last_periods = [7, 30, 60, 90, 365]
for p in average_last_periods:
    avg_pr = df['PR'].rolling(window=p).mean().iloc[-1]
    avg_text = f"Average PR last {p}-d: {avg_pr:.1f}%"
    ax.annotate(avg_text, xy=(0.995, 0.25 - 0.04 * average_last_periods.index(p)),
                xycoords='axes fraction', fontsize=10, ha='right')

# Show and save the plot
plt.savefig("plot.png", dpi=300)  # Specify the filename and DPI (dots per inch)
plt.show()
