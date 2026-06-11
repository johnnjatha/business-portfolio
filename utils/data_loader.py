import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

db = create_client(SUPABASE_URL, SUPABASE_KEY)

MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

SEED = [
  {
    "id":"arstern-analytics","name":"Arstern Analytics",
    "initials":"AA","color":"blue",
    "sector":"Data & MEAL Consultancy","location":"Nairobi, Kenya",
    "stage":"Building","founded":"2024","founder":"Sole founder",
    "description":"A Nairobi-based data consultancy delivering MEAL system design, market intelligence, and data science services to NGOs and businesses across East Africa.",
    "about":"Arstern Analytics is built on the founder's cross-disciplinary expertise in criminology, information management, cybersecurity, and MEAL.",
    "revenue_streams":[
      {"name":"MEAL consultancy","description":"M&E system design, data collection, reporting for NGOs","status":"Primary","status_color":"amber"},
      {"name":"Market intelligence","description":"Nairobi demand intelligence, sector trend reports","status":"Growing","status_color":"blue"},
      {"name":"Training & capacity building","description":"Data analysis, KoboToolbox, Python for MEAL","status":"Planned","status_color":"gray"}
    ],
    "setup_progress":[
      {"label":"Business concept","pct":100,"status":"Done"},
      {"label":"Business plan","pct":100,"status":"Done"},
      {"label":"Policy & governance docs","pct":100,"status":"Done"},
      {"label":"Formal registration","pct":40,"status":"In progress"},
      {"label":"First paying client","pct":0,"status":"Not started"}
    ],
    "plan":{
      "executive_summary":"Arstern Analytics is a Nairobi-based data consultancy delivering MEAL system design, market intelligence, and data science training to development sector organizations and businesses.",
      "problem_solution":"NGOs and SMEs in Kenya struggle with weak M&E systems, poor data quality, and limited analytical capacity. Arstern Analytics bridges this with end-to-end MEAL services.",
      "target_market":"Primary: Local and international NGOs in Kenya and East Africa. Secondary: SMEs needing market intelligence. Tertiary: Development sector professionals seeking upskilling.",
      "revenue_model":"Three streams: (1) Project-based MEAL consultancy fees. (2) Retainer contracts with NGOs. (3) Training workshops billed per cohort. Target: KES 150,000/month by end of Year 1.",
      "competitive_advantage":"Rare combination of MEAL expertise, data science, IT governance, and cybersecurity knowledge. Built-in credibility through prior NGO work (BlueBiz, KWETU).",
      "risks_mitigation":"Key risks: slow client acquisition, income inconsistency, competition. Mitigation: leverage existing NGO network, diversify across retainers and training."
    },
    "kpis":[
      {"indicator":"Monthly revenue","unit":"KES","target":"150,000","actual":"0","status":"Not started","status_color":"amber"},
      {"indicator":"Active clients","unit":"Count","target":"3","actual":"0","status":"Not started","status_color":"amber"},
      {"indicator":"Projects delivered","unit":"This year","target":"5","actual":"0","status":"Not started","status_color":"amber"},
      {"indicator":"Training cohorts","unit":"This year","target":"2","actual":"0","status":"Not started","status_color":"amber"},
      {"indicator":"Business registration","unit":"Milestone","target":"Q3 2026","actual":"—","status":"In progress","status_color":"blue"}
    ]
  },
  {
    "id":"tocare","name":"TOCARE",
    "initials":"TC","color":"teal",
    "sector":"NGO / Social Impact","location":"Nairobi, Kenya",
    "stage":"Idea stage","founded":"2024","founder":"Sole founder",
    "description":"An NGO concept focused on community care, social welfare, and development programming for vulnerable populations in Kenya.",
    "about":"TOCARE is being developed as a non-governmental organization with a mission centred on care, dignity, and community empowerment.",
    "revenue_streams":[
      {"name":"Donor grants","description":"Institutional funding from bilateral and multilateral donors","status":"Primary","status_color":"amber"},
      {"name":"Community programmes","description":"Funded social welfare and development projects","status":"Planned","status_color":"gray"},
      {"name":"Partnerships","description":"Co-implementation with NGO and government partners","status":"Planned","status_color":"gray"}
    ],
    "setup_progress":[
      {"label":"Organizational concept","pct":100,"status":"Done"},
      {"label":"Policy & governance suite","pct":100,"status":"Done"},
      {"label":"MEAL framework","pct":80,"status":"In progress"},
      {"label":"NGO registration","pct":10,"status":"Early stage"},
      {"label":"First funded project","pct":0,"status":"Not started"}
    ],
    "plan":{
      "executive_summary":"TOCARE is a Kenyan NGO concept focused on community care and social welfare programming, delivering evidence-based interventions for vulnerable populations.",
      "problem_solution":"Many Kenyan communities lack access to quality social welfare support. TOCARE addresses this through targeted community programmes with strong M&E systems.",
      "target_market":"Vulnerable populations in Kenya — youth, women, and low-income households. Institutional donors seeking credible local implementing partners.",
      "revenue_model":"Grant-based funding from bilateral donors (USAID, EU, FCDO), multilateral agencies (UNICEF, UNDP), and private foundations.",
      "competitive_advantage":"Strong institutional documentation, donor-ready MEAL systems, and deep development sector experience from the outset.",
      "risks_mitigation":"Key risks: competitive grant environment, long lead time to first funding. Mitigation: begin with small sub-grants, partner with established NGOs."
    },
    "kpis":[
      {"indicator":"NGO registration","unit":"Milestone","target":"Q4 2026","actual":"—","status":"Early stage","status_color":"amber"},
      {"indicator":"Grant applications submitted","unit":"Count","target":"3","actual":"0","status":"Not started","status_color":"amber"},
      {"indicator":"Partnerships established","unit":"Count","target":"2","actual":"0","status":"Not started","status_color":"amber"},
      {"indicator":"Beneficiaries reached","unit":"People","target":"500","actual":"0","status":"Not started","status_color":"amber"}
    ]
  }
]


def _seed_if_empty():
    result = db.table("businesses").select("id").execute()
    if not result.data:
        for biz in SEED:
            db.table("businesses").insert(biz).execute()


_seed_if_empty()


# ── Businesses ──────────────────────────────────────────────────

def load_businesses():
    result = db.table("businesses").select("*").execute()
    return result.data or []

def get_business(business_id):
    result = db.table("businesses").select("*").eq("id", business_id).execute()
    return result.data[0] if result.data else None

def save_business(updated):
    db.table("businesses").update(updated).eq("id", updated["id"]).execute()

def add_business(biz):
    db.table("businesses").insert(biz).execute()

def save_businesses(businesses):
    for biz in businesses:
        save_business(biz)

def delete_business_record(business_id):
    db.table("businesses").delete().eq("id", business_id).execute()
    db.table("revenue_log").delete().eq("business_id", business_id).execute()


# ── Revenue ─────────────────────────────────────────────────────

def load_revenue(business_id=None):
    query = db.table("revenue_log").select("*")
    if business_id:
        query = query.eq("business_id", business_id)
    result = query.execute()
    rows = []
    for row in (result.data or []):
        m = int(row["month"])
        rows.append({
            "business_id": row["business_id"],
            "year":   int(row["year"]),
            "month":  m,
            "amount": float(row["amount"]),
            "notes":  row.get("notes", "") or "",
            "month_label": MONTHS[m-1],
            "period": f"{MONTHS[m-1]} {row['year']}"
        })
    return sorted(rows, key=lambda r: (r["year"], r["month"]))

def save_revenue_entry(business_id, year, month, amount, notes=""):
    existing = db.table("revenue_log").select("id")\
        .eq("business_id", business_id)\
        .eq("year", year).eq("month", month).execute()
    if existing.data:
        db.table("revenue_log").update({"amount": amount, "notes": notes})\
            .eq("business_id", business_id)\
            .eq("year", year).eq("month", month).execute()
    else:
        db.table("revenue_log").insert({
            "business_id": business_id,
            "year": year, "month": month,
            "amount": amount, "notes": notes
        }).execute()

def delete_revenue_entry(business_id, year, month):
    db.table("revenue_log").delete()\
        .eq("business_id", business_id)\
        .eq("year", year).eq("month", month).execute()


# ── Summary helpers ─────────────────────────────────────────────

def revenue_summary(business_id):
    from datetime import datetime
    rows = load_revenue(business_id)
    if not rows:
        return {"total":0,"this_month":0,"last_month":0,
                "mom_change":None,"chart_labels":[],"chart_data":[],"rows":[]}
    total  = sum(r["amount"] for r in rows)
    now    = datetime.now()
    this_m = sum(r["amount"] for r in rows
                 if r["year"] == now.year and r["month"] == now.month)
    pm     = datetime(now.year, now.month-1, 1) if now.month > 1 else datetime(now.year-1, 12, 1)
    last_m = sum(r["amount"] for r in rows
                 if r["year"] == pm.year and r["month"] == pm.month)
    mom = round(((this_m - last_m) / last_m) * 100, 1) if last_m > 0 else None
    return {"total":total,"this_month":this_m,"last_month":last_m,
            "mom_change":mom,
            "chart_labels":[r["period"] for r in rows],
            "chart_data":  [r["amount"]  for r in rows],
            "rows":rows}

def portfolio_summary():
    businesses = load_businesses()
    total_rev  = sum(sum(r["amount"] for r in load_revenue(b["id"])) for b in businesses)
    return {"count":len(businesses),"total_revenue":total_rev,"businesses":businesses}
