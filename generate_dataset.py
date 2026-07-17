"""
generate_dataset.py
--------------------
Generates the MLALAD (MLA Local Area Development) fund dataset for
Amravati district, FY 2024-25.

REAL / SOURCED facts used:
  - Amravati district's 8 official assembly constituencies (source: District
    Election Officer, Amravati -- amravati.gov.in)
  - Maharashtra MLALAD annual entitlement of Rs 5 Crore per MLA per year
    (source: Business Standard, Oct 2024 -- "Maharashtra's Rs 1,830 crore
    with Rs 5 crore each for its 288 MLAs")
  - Eligible work categories per MLALADS guidelines (roads, drinking water,
    education, health, sanitation, community assets, sports facilities)

ILLUSTRATIVE (not real) fields, clearly flagged:
  - MLA identity -> anonymized to "MLA - <Constituency>" (real named
    politicians are deliberately NOT used -- see project notes)
  - Individual work-level sanctioned/spent amounts and dates
  - Exact utilization percentages

Run: python3 generate_dataset.py
Output: mla_fund_dataset.csv
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(7)

# ---------------------------------------------------------------
# 1. Real Amravati district assembly constituencies
#    (8 official ACs; a 9th generic slot added since the internship
#    dataset covered 9 MLAs -- rename if the 9th belongs to an
#    adjoining district)
# ---------------------------------------------------------------
constituencies = [
    "Amravati", "Badnera", "Teosa", "Daryapur",
    "Melghat", "Achalpur", "Morshi", "Dhamangaon",
    "Amravati (Additional Segment)",
]

mla_labels = [f"MLA - {c}" for c in constituencies]

ANNUAL_ENTITLEMENT = 5_00_00_000  # Rs 5 Crore, real MLALAD figure for Maharashtra

# ---------------------------------------------------------------
# 2. Spending categories (real MLALADS-eligible categories,
#    matched to what you described from your internship)
# ---------------------------------------------------------------
categories = {
    "Roads": 0.24,
    "Water Tank / Drinking Water": 0.15,
    "School Building & Equipment": 0.14,
    "Drainage": 0.12,
    "Community Hall": 0.10,
    "Playground": 0.09,
    "Compound Wall (Schools/Institutions)": 0.08,
    "Open Gym": 0.05,
    "Sanitation": 0.03,
}

work_templates = {
    "Roads": ["Cement concrete road, {v}", "Road widening near {v}", "Repair of approach road, {v}"],
    "Water Tank / Drinking Water": ["Overhead water tank construction, {v}", "Bore-well installation, {v}"],
    "School Building & Equipment": ["Additional classroom, ZP School {v}", "Furniture & equipment supply, {v} school",
                                     "Smart-class equipment, {v} school"],
    "Drainage": ["Drainage line construction, {v}", "Nala (drain) improvement, {v}"],
    "Community Hall": ["Construction of community hall, {v}", "Renovation of Samaj Mandir, {v}"],
    "Playground": ["Development of playground, {v}", "Playground boundary & leveling, {v}"],
    "Compound Wall (Schools/Institutions)": ["Compound wall, ZP School {v}", "Compound wall, {v} Primary Health Centre"],
    "Open Gym": ["Open-air gym installation, {v}", "Outdoor fitness equipment, {v}"],
    "Sanitation": ["Public toilet block, {v}", "Solid waste collection point, {v}"],
}

villages = ["Nandgaon", "Chandur", "Talegaon", "Rasulabad", "Shendurjana",
            "Walgaon", "Anjangaon", "Paratwada", "Chikhaldara", "Warud",
            "Dabhada", "Kholapur", "Kurha", "Nimbhora", "Yavali"]

status_options = ["Completed", "In Progress", "Delayed", "Not Started"]
status_weights = [0.55, 0.24, 0.15, 0.06]

FY = "2024-25"

# ---------------------------------------------------------------
# 3. Generate work-level records per MLA
# ---------------------------------------------------------------
rows = []
work_counter = 1

for mla_label, constituency in zip(mla_labels, constituencies):
    n_works = np.random.randint(10, 16)  # keep it light/minimal, not overloaded
    utilization_factor = np.random.uniform(0.60, 0.95)  # not every MLA spends full fund
    total_sanctioned_this_year = ANNUAL_ENTITLEMENT * utilization_factor
    weights = np.random.dirichlet(np.ones(n_works))
    work_amounts = (weights * total_sanctioned_this_year).round(-3)

    for amt in work_amounts:
        category = np.random.choice(list(categories.keys()), p=list(categories.values()))
        village = np.random.choice(villages)
        desc = np.random.choice(work_templates[category]).format(v=village)

        sanction_date = datetime(2024, np.random.randint(4, 13), np.random.randint(1, 28)) \
            if True else None
        status = np.random.choice(status_options, p=status_weights)

        if status == "Completed":
            spent_pct = np.random.uniform(0.90, 1.0)
        elif status == "In Progress":
            spent_pct = np.random.uniform(0.35, 0.85)
        elif status == "Delayed":
            spent_pct = np.random.uniform(0.10, 0.55)
        else:
            spent_pct = 0.0

        spent_amount = round(amt * spent_pct, -2)

        rows.append({
            "Work_ID": f"WRK{work_counter:04d}",
            "MLA": mla_label,
            "Constituency": constituency,
            "District": "Amravati",
            "Financial_Year": FY,
            "Category": category,
            "Work_Description": desc,
            "Village": village,
            "Sanctioned_Amount": int(amt),
            "Spent_Amount": int(spent_amount),
            "Remaining_Balance": int(amt - spent_amount),
            "Sanction_Date": sanction_date.strftime("%Y-%m-%d"),
            "Status": status,
        })
        work_counter += 1

df = pd.DataFrame(rows)
df.to_csv("mla_fund_dataset.csv", index=False)

print(f"Generated {len(df)} work records for {len(mla_labels)} MLAs, FY {FY}.")
print(df.head())
