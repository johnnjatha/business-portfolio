# Business Portfolio Tracker

A responsive Flask web app to track, plan, and measure all your business ventures — on desktop and mobile.

---

## Setup (one time)

```bash
# 1. Navigate to the project folder
cd business_portfolio

# 2. Install Flask
pip install -r requirements.txt

# 3. Run the app
python app.py
```

Then open your browser at: **http://localhost:5000**

---

## Features

| Feature | Description |
|---|---|
| Portfolio overview | Card grid of all your businesses with status badges |
| Business detail | Full profile with 4 tabs: Overview, Plan, Revenue, KPIs |
| Business plan | 6-section lean startup plan, accordion + full-page view |
| Revenue tracker | Monthly log table + Chart.js bar chart with MoM growth |
| KPI indicators | Add/edit/delete indicators, track target vs actual |
| Revenue streams | Add income streams per business with status tags |
| Setup progress | Visual progress bars with inline slider updates |
| Flash messages | Success/error feedback on every action |
| Add / Edit / Delete | Full CRUD for businesses, KPIs, revenue entries, streams |
| Responsive design | Desktop sidebar nav + mobile bottom nav + drawer |

---

## Project structure

```
business_portfolio/
├── app.py                  ← Flask routes (all 15 endpoints)
├── requirements.txt
├── README.md
├── data/
│   ├── businesses.json     ← All business data (auto-saved)
│   └── revenue_log.csv     ← Monthly revenue entries
├── utils/
│   └── data_loader.py      ← Read/write helpers for all data
├── templates/
│   ├── base.html           ← Layout: sidebar, mobile nav, flash
│   ├── index.html          ← Portfolio home / overview
│   ├── business_detail.html ← Tabbed business page
│   ├── business_plan.html  ← Full plan view
│   ├── add_business.html   ← Add new venture form
│   └── edit_business.html  ← Edit existing business
└── static/
    ├── css/style.css       ← All styles, responsive breakpoints
    └── js/main.js          ← Tabs, accordion, charts, flash
```

---

## Pre-loaded businesses

- **Arstern Analytics** — Data & MEAL consultancy (Building)
- **TOCARE** — NGO / Social impact (Idea stage)

---

## How to add a new business

1. Click **+ Add business** in the sidebar or home page
2. Fill in name, sector, stage, and plan sections
3. Go to the KPIs tab to set your indicators and targets
4. Log revenue entries under the Revenue tab as income comes in

---

## Data storage

All data is stored locally as flat files — no database required:
- `businesses.json` — business profiles, plans, KPIs, streams, progress
- `revenue_log.csv` — one row per business per month

To back up your data, copy the `data/` folder.
