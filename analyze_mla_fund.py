"""
analyze_mla_fund.py
--------------------
Generates key insights for the Amravati MLALAD dataset, FY 2024-25.
Outputs:
  - insights_summary.xlsx (3 sheets)
  - charts/*.png (minimal style, single accent color)

Run: python3 analyze_mla_fund.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

os.makedirs("charts", exist_ok=True)

df = pd.read_csv("mla_fund_dataset.csv")

# ---------- Minimal style ----------
plt.rcParams.update({
    "font.family": "sans-serif",
    "axes.edgecolor": "#DDDDDD",
    "axes.linewidth": 0.8,
    "axes.grid": True,
    "grid.color": "#EEEEEE",
    "grid.linewidth": 0.6,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "text.color": "#2B2B2B",
    "axes.labelcolor": "#2B2B2B",
    "xtick.color": "#555555",
    "ytick.color": "#555555",
})

ACCENT = "#3E6D9C"      # muted blue
ACCENT2 = "#C97B4A"     # muted terracotta (secondary)
PALETTE = ["#3E6D9C", "#6E9CC4", "#9DC0DD", "#C97B4A", "#D9A679",
           "#7FA98E", "#B7B7B7", "#556270", "#E0C097"]

# ---------------------------------------------------------------
# 1. MLA-wise summary
# ---------------------------------------------------------------
mla_summary = (
    df.groupby(["MLA", "Constituency"])
    .agg(Sanctioned=("Sanctioned_Amount", "sum"),
         Spent=("Spent_Amount", "sum"),
         Works=("Work_ID", "count"))
    .reset_index()
)
mla_summary["Remaining"] = mla_summary["Sanctioned"] - mla_summary["Spent"]
mla_summary["Utilization_%"] = (mla_summary["Spent"] / mla_summary["Sanctioned"] * 100).round(1)
mla_summary = mla_summary.sort_values("Utilization_%", ascending=False)

# ---------------------------------------------------------------
# 2. Category-wise summary
# ---------------------------------------------------------------
category_summary = (
    df.groupby("Category")
    .agg(Sanctioned=("Sanctioned_Amount", "sum"), Spent=("Spent_Amount", "sum"))
    .reset_index()
    .sort_values("Spent", ascending=False)
)

# ---------------------------------------------------------------
# 3. Status summary
# ---------------------------------------------------------------
status_summary = df["Status"].value_counts(normalize=True).mul(100).round(1).reset_index()
status_summary.columns = ["Status", "Percentage"]

with pd.ExcelWriter("insights_summary.xlsx", engine="openpyxl") as writer:
    mla_summary.to_excel(writer, sheet_name="MLA_Summary", index=False)
    category_summary.to_excel(writer, sheet_name="Category_Summary", index=False)
    status_summary.to_excel(writer, sheet_name="Status_Summary", index=False)

print("Saved insights_summary.xlsx")

# ---------------------------------------------------------------
# Chart 1: MLA-wise utilization (horizontal, minimal)
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5.5))
y = range(len(mla_summary))
ax.barh(y, mla_summary["Utilization_%"], color=ACCENT, height=0.55)
ax.set_yticks(y)
ax.set_yticklabels(mla_summary["Constituency"])
ax.invert_yaxis()
ax.set_xlabel("Fund Utilization (%)")
ax.set_title("Fund Utilization by Constituency — FY 2024-25", loc="left", fontsize=13, weight="bold")
for i, v in enumerate(mla_summary["Utilization_%"]):
    ax.text(v + 1, i, f"{v}%", va="center", fontsize=9, color="#555555")
ax.set_xlim(0, 100)
plt.tight_layout()
plt.savefig("charts/1_utilization_by_constituency.png", dpi=160)
plt.close()

# ---------------------------------------------------------------
# Chart 2: Category-wise spend (horizontal bar, minimal — avoids
# busy pie charts)
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5.5))
cat_sorted = category_summary.sort_values("Spent")
ax.barh(cat_sorted["Category"], cat_sorted["Spent"] / 1e5, color=ACCENT2, height=0.55)
ax.set_xlabel("Amount Spent (Rs. Lakh)")
ax.set_title("Spend by Category — FY 2024-25", loc="left", fontsize=13, weight="bold")
plt.tight_layout()
plt.savefig("charts/2_category_spend.png", dpi=160)
plt.close()

# ---------------------------------------------------------------
# Chart 3: Sanctioned vs Spent per constituency (grouped, minimal)
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 5.5))
x = range(len(mla_summary))
w = 0.35
ax.bar([i - w/2 for i in x], mla_summary["Sanctioned"] / 1e7, width=w, label="Sanctioned", color="#C9D6E3")
ax.bar([i + w/2 for i in x], mla_summary["Spent"] / 1e7, width=w, label="Spent", color=ACCENT)
ax.set_xticks(x)
ax.set_xticklabels(mla_summary["Constituency"], rotation=30, ha="right")
ax.set_ylabel("Amount (Rs. Crore)")
ax.set_title("Sanctioned vs Spent by Constituency — FY 2024-25", loc="left", fontsize=13, weight="bold")
ax.legend(frameon=False)
plt.tight_layout()
plt.savefig("charts/3_sanctioned_vs_spent.png", dpi=160)
plt.close()

# ---------------------------------------------------------------
# Chart 4: Work status (simple horizontal stacked bar, not pie)
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 1.8))
left = 0
status_colors = {"Completed": "#3E6D9C", "In Progress": "#9DC0DD",
                  "Delayed": "#C97B4A", "Not Started": "#D9D9D9"}
for _, row in status_summary.sort_values("Status").iterrows():
    ax.barh(0, row["Percentage"], left=left, color=status_colors.get(row["Status"], "#999999"),
             label=f"{row['Status']} ({row['Percentage']}%)", height=0.5)
    left += row["Percentage"]
ax.set_yticks([])
ax.set_xlim(0, 100)
ax.set_title("Work Status Distribution — All Constituencies", loc="left", fontsize=13, weight="bold")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.4), ncol=4, frameon=False, fontsize=8)
plt.tight_layout()
plt.savefig("charts/4_status_distribution.png", dpi=160, bbox_inches="tight")
plt.close()

print("Saved 4 minimal charts in /charts")

# ---------------------------------------------------------------
# Headline insights
# ---------------------------------------------------------------
total_sanctioned = df["Sanctioned_Amount"].sum()
total_spent = df["Spent_Amount"].sum()
util = round(total_spent / total_sanctioned * 100, 1)

print("\n===== HEADLINE INSIGHTS =====")
print(f"Total Sanctioned (9 MLAs, FY 2024-25): Rs {total_sanctioned:,}")
print(f"Total Spent: Rs {total_spent:,}")
print(f"Overall Utilization: {util}%")
print(f"Unspent / Remaining: Rs {total_sanctioned - total_spent:,}")
print(f"Top spending category: {category_summary.iloc[0]['Category']}")
print(f"Highest utilization: {mla_summary.iloc[0]['Constituency']} ({mla_summary.iloc[0]['Utilization_%']}%)")
print(f"Lowest utilization: {mla_summary.iloc[-1]['Constituency']} ({mla_summary.iloc[-1]['Utilization_%']}%)")
