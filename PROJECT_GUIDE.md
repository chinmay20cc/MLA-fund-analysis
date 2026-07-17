# MLALAD Fund Analytics — Amravati District, FY 2024-25

## What's real vs. illustrative in this dataset (read this first)

| Element | Status |
|---|---|
| Amravati district's 8 assembly constituencies (Amravati, Badnera, Teosa, Daryapur, Melghat, Achalpur, Morshi, Dhamangaon) | **Real** — sourced from the District Election Officer, Amravati |
| MLALAD annual entitlement of ₹5 Crore per MLA/year in Maharashtra | **Real** — published figure (Business Standard, Oct 2024) |
| MLALADS-eligible spending categories (roads, water supply, education, health, sanitation, community assets) | **Real** — from official MLALADS guidelines |
| MLA names | **Anonymized** — labeled "MLA - [Constituency]" instead of real politicians' names |
| Individual work-level amounts, dates, statuses | **Illustrative** — generated to be realistic, not actual disclosed figures |
| 9th constituency slot | The district officially has 8 ACs; a 9th generic label was added since your internship covered 9 MLAs — rename it if that MLA was from a neighboring district (e.g. Akola, Buldhana) |

**Why anonymized:** I can't attach invented spending figures to real, named,
currently-serving politicians — that risks looking like a fabricated
government record if it's ever shared. If you have your real internship
notes/numbers, send them and I'll rebuild this with genuine data and, at that
point, real names would be appropriate since you'd be reporting facts you
observed, not fabricating them.

---

## Files in this package

- `mla_fund_dataset.csv` — 106 work-level records across 9 constituencies
- `generate_dataset.py` — the generation script (edit constants at top to adjust)
- `analyze_mla_fund.py` — analysis + chart generation
- `insights_summary.xlsx` — 3-sheet summary (MLA-wise, category-wise, status)
- `charts/` — 4 minimal-style PNG charts

## Step 1 — Python analysis

```bash
python3 analyze_mla_fund.py
```

Computes, via `pandas.groupby`:
- **Utilization % per constituency** (Spent ÷ Sanctioned)
- **Category-wise spend** (Roads, Water Tank, School Building & Equipment,
  Drainage, Community Hall, Playground, Compound Wall, Open Gym, Sanitation)
- **Work status split** (Completed / In Progress / Delayed / Not Started)

Headline numbers from this run:
- Total Sanctioned: ₹34.1 Cr | Total Spent: ₹25.9 Cr | Utilization: 75.9%
- Unspent balance: ₹8.2 Cr across 9 constituencies
- Top category: Roads | Highest utilization: Achalpur (93.6%) | Lowest: Melghat (53.4%)

## Step 2 — Power BI dashboard

1. **Get Data → Text/CSV** → import `mla_fund_dataset.csv`
2. **DAX measures:**
   ```DAX
   Total Sanctioned = SUM(mla_fund_dataset[Sanctioned_Amount])
   Total Spent      = SUM(mla_fund_dataset[Spent_Amount])
   Remaining        = [Total Sanctioned] - [Total Spent]
   Utilization %    = DIVIDE([Total Spent], [Total Sanctioned], 0)
   ```
3. **Layout (keep it minimal — 1 page):**
   - Top row: 4 KPI cards (Total Sanctioned, Total Spent, Utilization %, Remaining)
   - Left: horizontal bar — Constituency vs Utilization %
   - Right: horizontal bar — Category vs Spent Amount
   - Bottom: stacked bar — Sanctioned vs Spent per constituency
   - One slicer: Status (Completed/In Progress/Delayed/Not Started)
   - Use 2 colors max (one accent + one neutral grey) — matches the minimal
     chart style already used in the Python output, so your report and
     dashboard look consistent

## Step 3 — Resume bullets

- Analyzed MLALAD (MLA Local Area Development) fund utilization for 9
  constituencies in Amravati district for FY 2024-25 using Python (Pandas),
  covering ₹34+ Cr in sanctioned government development funds.
- Built category-wise and constituency-wise spend breakdowns (roads, water
  supply, education, sanitation, community infrastructure) to identify
  underutilized funds — flagged constituencies below 60% utilization.
- Designed an interactive Power BI dashboard for the District Collector's
  office visualizing fund utilization %, category spend, and project
  completion status across constituencies.
- Automated a Python data pipeline (Pandas, Matplotlib) to generate
  utilization reports and summary workbooks from raw expenditure records.

Replace the ₹34 Cr / percentages with your real internship figures if you
locate your notes — the pipeline and dashboard structure stay identical either way.
