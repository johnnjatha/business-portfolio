import json
import csv
import os
from datetime import datetime

DATA_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data"))
BUSINESSES_FILE = os.path.join(DATA_DIR, "businesses.json")
REVENUE_FILE = os.path.join(DATA_DIR, "revenue_log.csv")

MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]


def load_businesses():
    with open(BUSINESSES_FILE, "r") as f:
        return json.load(f)


def get_business(business_id):
    businesses = load_businesses()
    return next((b for b in businesses if b["id"] == business_id), None)


def save_businesses(businesses):
    with open(BUSINESSES_FILE, "w") as f:
        json.dump(businesses, f, indent=2)


def save_business(updated):
    businesses = load_businesses()
    for i, b in enumerate(businesses):
        if b["id"] == updated["id"]:
            businesses[i] = updated
            break
    save_businesses(businesses)


def add_business(business):
    businesses = load_businesses()
    businesses.append(business)
    save_businesses(businesses)


def load_revenue(business_id=None):
    rows = []
    if not os.path.exists(REVENUE_FILE):
        return rows
    with open(REVENUE_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if business_id is None or row["business_id"] == business_id:
                rows.append({
                    "business_id": row["business_id"],
                    "year": int(row["year"]),
                    "month": int(row["month"]),
                    "amount": float(row["amount"]),
                    "notes": row.get("notes", ""),
                    "month_label": MONTHS[int(row["month"]) - 1],
                    "period": f"{MONTHS[int(row['month'])-1]} {row['year']}"
                })
    return sorted(rows, key=lambda r: (r["year"], r["month"]))


def save_revenue_entry(business_id, year, month, amount, notes=""):
    rows = []
    exists = False
    if os.path.exists(REVENUE_FILE):
        with open(REVENUE_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["business_id"] == business_id and int(row["year"]) == int(year) and int(row["month"]) == int(month):
                    row["amount"] = amount
                    row["notes"] = notes
                    exists = True
                rows.append(row)
    if not exists:
        rows.append({"business_id": business_id, "year": year, "month": month, "amount": amount, "notes": notes})
    with open(REVENUE_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["business_id", "year", "month", "amount", "notes"])
        writer.writeheader()
        writer.writerows(rows)


def delete_revenue_entry(business_id, year, month):
    rows = []
    if os.path.exists(REVENUE_FILE):
        with open(REVENUE_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not (row["business_id"] == business_id and int(row["year"]) == int(year) and int(row["month"]) == int(month)):
                    rows.append(row)
    with open(REVENUE_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["business_id", "year", "month", "amount", "notes"])
        writer.writeheader()
        writer.writerows(rows)


def revenue_summary(business_id):
    rows = load_revenue(business_id)
    if not rows:
        return {"total": 0, "this_month": 0, "last_month": 0, "mom_change": None, "chart_labels": [], "chart_data": []}
    total = sum(r["amount"] for r in rows)
    now = datetime.now()
    this_month = sum(r["amount"] for r in rows if r["year"] == now.year and r["month"] == now.month)
    last_month_dt = datetime(now.year, now.month - 1, 1) if now.month > 1 else datetime(now.year - 1, 12, 1)
    last_month = sum(r["amount"] for r in rows if r["year"] == last_month_dt.year and r["month"] == last_month_dt.month)
    mom_change = None
    if last_month > 0:
        mom_change = round(((this_month - last_month) / last_month) * 100, 1)
    return {
        "total": total,
        "this_month": this_month,
        "last_month": last_month,
        "mom_change": mom_change,
        "chart_labels": [r["period"] for r in rows],
        "chart_data": [r["amount"] for r in rows],
        "rows": rows
    }


def portfolio_summary():
    businesses = load_businesses()
    total_revenue = 0
    for b in businesses:
        rev = load_revenue(b["id"])
        total_revenue += sum(r["amount"] for r in rev)
    return {
        "count": len(businesses),
        "total_revenue": total_revenue,
        "businesses": businesses
    }
