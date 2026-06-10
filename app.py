import os, sys, json, csv
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash

# ── Windows path fix ────────────────────────────────────────────
BASE_DIR        = os.path.dirname(os.path.abspath(__file__))
DATA_DIR        = os.path.join(BASE_DIR, "data")
BUSINESSES_FILE = os.path.join(DATA_DIR, "businesses.json")
REVENUE_FILE    = os.path.join(DATA_DIR, "revenue_log.csv")
MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

# ── Auto-create data folder + seed files on first run ───────────
def _init_data():
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(REVENUE_FILE):
        with open(REVENUE_FILE, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(["business_id","year","month","amount","notes"])

    if not os.path.exists(BUSINESSES_FILE):
        seed = [
          {
            "id":"arstern-analytics","name":"Arstern Analytics",
            "initials":"AA","color":"blue",
            "sector":"Data & MEAL Consultancy","location":"Nairobi, Kenya",
            "stage":"Building","founded":"2024","founder":"Sole founder",
            "description":"A Nairobi-based data consultancy delivering MEAL system design, market intelligence, and data science services to NGOs and businesses across East Africa.",
            "about":"Arstern Analytics is built on the founder's cross-disciplinary expertise in criminology, information management, cybersecurity, and MEAL — combining rigorous data methodology with on-the-ground programme experience.",
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
              "executive_summary":"Arstern Analytics is a Nairobi-based data consultancy delivering MEAL system design, market intelligence, and data science training to development sector organizations and businesses. The firm targets a growing gap in quality, affordable data services across East Africa's NGO and SME ecosystem.",
              "problem_solution":"NGOs and SMEs in Kenya struggle with weak M&E systems, poor data quality, and limited analytical capacity. Arstern Analytics bridges this with end-to-end MEAL services — from tool design (KoboToolbox, ODK) to dashboard visualization (Looker Studio, Python) — at consultancy rates accessible to mid-tier organizations.",
              "target_market":"Primary: Local and international NGOs operating in Kenya and East Africa requiring MEAL system support. Secondary: SMEs and startups needing market intelligence and data-driven decision support. Tertiary: Development sector professionals seeking upskilling in data tools.",
              "revenue_model":"Three streams: (1) Project-based MEAL consultancy fees billed per engagement. (2) Retainer contracts with NGOs for ongoing data management. (3) Training workshops billed per cohort. Target: KES 150,000/month by end of Year 1.",
              "competitive_advantage":"Rare combination of MEAL expertise, data science capability, IT governance, and cybersecurity knowledge. Built-in credibility through prior NGO programme work (BlueBiz, KWETU). Ability to deliver end-to-end without needing multiple vendors.",
              "risks_mitigation":"Key risks: slow client acquisition as a new firm, income inconsistency from project-based billing, and competition from established consultancies. Mitigation: leverage existing NGO network for early contracts, diversify across retainers and training, build a public portfolio to demonstrate capability."
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
            "about":"TOCARE is being developed as a non-governmental organization with a mission centred on care, dignity, and community empowerment, drawing on the founder's development sector experience.",
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
              "executive_summary":"TOCARE is a Kenyan NGO concept focused on community care and social welfare programming, delivering evidence-based interventions for vulnerable populations through well-structured programmes anchored in strong MEAL systems.",
              "problem_solution":"Many Kenyan communities lack access to quality social welfare support. TOCARE addresses this through targeted community programmes, leveraging strong M&E systems to demonstrate impact to donors and stakeholders.",
              "target_market":"Vulnerable populations in Kenya — youth, women, and low-income households. Institutional donors and foundations seeking credible local implementing partners with strong accountability frameworks.",
              "revenue_model":"Grant-based funding from bilateral donors (USAID, EU, FCDO), multilateral agencies (UNICEF, UNDP), and private foundations. Co-funding arrangements with government line ministries for community programmes.",
              "competitive_advantage":"Strong institutional documentation, donor-ready MEAL systems, and deep development sector experience from the outset. Positions TOCARE as a credible, accountable partner from day one.",
              "risks_mitigation":"Key risks: competitive grant environment, long lead time to first funding, and capacity constraints as a startup NGO. Mitigation: begin with small sub-grants, partner with established NGOs, and build a demonstrable track record through community-level programming."
            },
            "kpis":[
              {"indicator":"NGO registration","unit":"Milestone","target":"Q4 2026","actual":"—","status":"Early stage","status_color":"amber"},
              {"indicator":"Grant applications submitted","unit":"Count","target":"3","actual":"0","status":"Not started","status_color":"amber"},
              {"indicator":"Partnerships established","unit":"Count","target":"2","actual":"0","status":"Not started","status_color":"amber"},
              {"indicator":"Beneficiaries reached","unit":"People","target":"500","actual":"0","status":"Not started","status_color":"amber"}
            ]
          }
        ]
        with open(BUSINESSES_FILE, "w", encoding="utf-8") as f:
            json.dump(seed, f, indent=2)

_init_data()  # runs automatically every startup — safe to run repeatedly

# ══════════════════════════════════════════════════════════════════
#  DATA HELPERS
# ══════════════════════════════════════════════════════════════════

def load_businesses():
    with open(BUSINESSES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_businesses(data):
    with open(BUSINESSES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def get_business(business_id):
    return next((b for b in load_businesses() if b["id"] == business_id), None)

def save_business(updated):
    data = load_businesses()
    for i, b in enumerate(data):
        if b["id"] == updated["id"]:
            data[i] = updated
            break
    save_businesses(data)

def add_business_data(biz):
    data = load_businesses()
    data.append(biz)
    save_businesses(data)

def load_revenue(business_id=None):
    rows = []
    if not os.path.exists(REVENUE_FILE):
        return rows
    with open(REVENUE_FILE, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if business_id is None or row["business_id"] == business_id:
                m = int(row["month"])
                rows.append({
                    "business_id": row["business_id"],
                    "year":   int(row["year"]),
                    "month":  m,
                    "amount": float(row["amount"]),
                    "notes":  row.get("notes",""),
                    "month_label": MONTHS[m-1],
                    "period": f"{MONTHS[m-1]} {row['year']}"
                })
    return sorted(rows, key=lambda r: (r["year"], r["month"]))

def save_revenue_entry(business_id, year, month, amount, notes=""):
    rows = []
    exists = False
    if os.path.exists(REVENUE_FILE):
        with open(REVENUE_FILE, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if (row["business_id"] == business_id and
                        int(row["year"]) == int(year) and
                        int(row["month"]) == int(month)):
                    row["amount"] = amount
                    row["notes"]  = notes
                    exists = True
                rows.append(row)
    if not exists:
        rows.append({"business_id":business_id,"year":year,
                     "month":month,"amount":amount,"notes":notes})
    with open(REVENUE_FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["business_id","year","month","amount","notes"])
        w.writeheader(); w.writerows(rows)

def delete_revenue_entry(business_id, year, month):
    rows = []
    if os.path.exists(REVENUE_FILE):
        with open(REVENUE_FILE, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if not (row["business_id"] == business_id and
                        int(row["year"]) == int(year) and
                        int(row["month"]) == int(month)):
                    rows.append(row)
    with open(REVENUE_FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["business_id","year","month","amount","notes"])
        w.writeheader(); w.writerows(rows)

def revenue_summary(business_id):
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

# ══════════════════════════════════════════════════════════════════
#  FLASK APP
# ══════════════════════════════════════════════════════════════════

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "arstern-portfolio-2024"

@app.context_processor
def inject_globals():
    return dict(businesses=load_businesses(), enumerate=enumerate)

# ── Portfolio home ──────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html", summary=portfolio_summary())

# ── Business detail ─────────────────────────────────────────────
@app.route("/business/<business_id>")
def business_detail(business_id):
    biz = get_business(business_id)
    if not biz:
        flash("Business not found.", "error")
        return redirect(url_for("index"))
    return render_template("business_detail.html",
                           biz=biz, rev=revenue_summary(business_id),
                           tab=request.args.get("tab","overview"))

# ── Full business plan ──────────────────────────────────────────
@app.route("/business/<business_id>/plan")
def business_plan(business_id):
    biz = get_business(business_id)
    if not biz: return redirect(url_for("index"))
    return render_template("business_plan.html", biz=biz)

# ── Add business ────────────────────────────────────────────────
@app.route("/add", methods=["GET","POST"])
def add_business_view():
    if request.method == "POST":
        f    = request.form
        name = f.get("name","").strip()
        if not name:
            flash("Business name is required.","error")
            return render_template("add_business.html")
        slug = name.lower().replace(" ","-").replace("&","and").replace("/","-")
        existing = [b["id"] for b in load_businesses()]
        base, n  = slug, 2
        while slug in existing:
            slug = f"{base}-{n}"; n += 1
        biz = {
            "id":slug,"name":name,
            "initials":"".join([w[0] for w in name.split()[:2]]).upper(),
            "color":f.get("color","blue"),"sector":f.get("sector",""),
            "location":f.get("location","Nairobi, Kenya"),
            "stage":f.get("stage","Idea stage"),"founded":f.get("founded","2024"),
            "founder":f.get("founder","Sole founder"),
            "description":f.get("description",""),"about":f.get("about",""),
            "revenue_streams":[],
            "setup_progress":[
                {"label":"Business concept","pct":0,"status":"Not started"},
                {"label":"Business plan","pct":0,"status":"Not started"},
                {"label":"Formal registration","pct":0,"status":"Not started"},
                {"label":"First client / funder","pct":0,"status":"Not started"},
            ],
            "plan":{
                "executive_summary":f.get("exec_summary",""),
                "problem_solution":f.get("problem_solution",""),
                "target_market":f.get("target_market",""),
                "revenue_model":f.get("revenue_model",""),
                "competitive_advantage":f.get("competitive_advantage",""),
                "risks_mitigation":f.get("risks_mitigation",""),
            },
            "kpis":[]
        }
        add_business_data(biz)
        flash(f"{name} added to your portfolio.","success")
        return redirect(url_for("business_detail", business_id=slug))
    return render_template("add_business.html")

# ── Edit business ───────────────────────────────────────────────
@app.route("/business/<business_id>/edit", methods=["GET","POST"])
def edit_business(business_id):
    biz = get_business(business_id)
    if not biz: return redirect(url_for("index"))
    if request.method == "POST":
        f = request.form
        biz["name"]        = f.get("name",biz["name"]).strip()
        biz["sector"]      = f.get("sector",biz["sector"])
        biz["location"]    = f.get("location",biz["location"])
        biz["stage"]       = f.get("stage",biz["stage"])
        biz["founded"]     = f.get("founded",biz["founded"])
        biz["founder"]     = f.get("founder",biz["founder"])
        biz["color"]       = f.get("color",biz.get("color","blue"))
        biz["description"] = f.get("description",biz["description"])
        biz["about"]       = f.get("about",biz["about"])
        biz["plan"]["executive_summary"]     = f.get("exec_summary","")
        biz["plan"]["problem_solution"]      = f.get("problem_solution","")
        biz["plan"]["target_market"]         = f.get("target_market","")
        biz["plan"]["revenue_model"]         = f.get("revenue_model","")
        biz["plan"]["competitive_advantage"] = f.get("competitive_advantage","")
        biz["plan"]["risks_mitigation"]      = f.get("risks_mitigation","")
        save_business(biz)
        flash("Changes saved.","success")
        return redirect(url_for("business_detail", business_id=business_id))
    return render_template("edit_business.html", biz=biz)

# ── Delete business ─────────────────────────────────────────────
@app.route("/business/<business_id>/delete", methods=["POST"])
def delete_business(business_id):
    businesses = load_businesses()
    name = next((b["name"] for b in businesses if b["id"] == business_id), business_id)
    save_businesses([b for b in businesses if b["id"] != business_id])
    flash(f"{name} removed from your portfolio.","success")
    return redirect(url_for("index"))

# ── Revenue: add ────────────────────────────────────────────────
@app.route("/business/<business_id>/revenue/add", methods=["POST"])
def add_revenue(business_id):
    f = request.form
    year, month, amount = f.get("year"), f.get("month"), f.get("amount")
    if year and month and amount:
        try:
            save_revenue_entry(business_id, int(year), int(month),
                               float(amount), f.get("notes",""))
            flash("Revenue entry saved.","success")
        except ValueError:
            flash("Invalid amount.","error")
    else:
        flash("Year, month and amount are required.","error")
    return redirect(url_for("business_detail", business_id=business_id, tab="revenue"))

# ── Revenue: delete ─────────────────────────────────────────────
@app.route("/business/<business_id>/revenue/delete", methods=["POST"])
def delete_revenue(business_id):
    f = request.form
    if f.get("year") and f.get("month"):
        delete_revenue_entry(business_id, int(f["year"]), int(f["month"]))
        flash("Entry deleted.","success")
    return redirect(url_for("business_detail", business_id=business_id, tab="revenue"))

# ── KPI: add ────────────────────────────────────────────────────
@app.route("/business/<business_id>/kpi/add", methods=["POST"])
def add_kpi(business_id):
    biz = get_business(business_id)
    if biz:
        indicator = request.form.get("indicator","").strip()
        if not indicator:
            flash("Indicator name is required.","error")
            return redirect(url_for("business_detail", business_id=business_id, tab="kpis"))
        biz["kpis"].append({
            "indicator":indicator,"unit":request.form.get("unit",""),
            "target":request.form.get("target",""),"actual":"0",
            "status":"Not started","status_color":"amber"
        })
        save_business(biz)
        flash(f"KPI '{indicator}' added.","success")
    return redirect(url_for("business_detail", business_id=business_id, tab="kpis"))

# ── KPI: update ─────────────────────────────────────────────────
@app.route("/business/<business_id>/kpi/update", methods=["POST"])
def update_kpi(business_id):
    biz = get_business(business_id)
    if biz:
        idx = int(request.form.get("idx",-1))
        if 0 <= idx < len(biz["kpis"]):
            status = request.form.get("status","Not started")
            biz["kpis"][idx]["actual"] = request.form.get("actual","0")
            biz["kpis"][idx]["status"] = status
            biz["kpis"][idx]["status_color"] = {
                "Not started":"amber","In progress":"blue",
                "On track":"green","Done":"green","At risk":"coral"
            }.get(status,"amber")
            save_business(biz)
            flash("KPI updated.","success")
    return redirect(url_for("business_detail", business_id=business_id, tab="kpis"))

# ── KPI: delete ─────────────────────────────────────────────────
@app.route("/business/<business_id>/kpi/delete", methods=["POST"])
def delete_kpi(business_id):
    biz = get_business(business_id)
    if biz:
        idx = int(request.form.get("idx",-1))
        if 0 <= idx < len(biz["kpis"]):
            removed = biz["kpis"].pop(idx)
            save_business(biz)
            flash(f"KPI '{removed['indicator']}' removed.","success")
    return redirect(url_for("business_detail", business_id=business_id, tab="kpis"))

# ── Revenue stream: add ─────────────────────────────────────────
@app.route("/business/<business_id>/stream/add", methods=["POST"])
def add_stream(business_id):
    biz = get_business(business_id)
    if biz:
        name = request.form.get("stream_name","").strip()
        if name:
            status = request.form.get("stream_status","Planned")
            biz["revenue_streams"].append({
                "name":name,"description":request.form.get("stream_desc",""),
                "status":status,
                "status_color":{"Primary":"amber","Growing":"blue",
                                "Active":"green","Planned":"gray"}.get(status,"gray")
            })
            save_business(biz)
            flash(f"Stream '{name}' added.","success")
    return redirect(url_for("business_detail", business_id=business_id, tab="overview"))

# ── Revenue stream: delete ──────────────────────────────────────
@app.route("/business/<business_id>/stream/delete", methods=["POST"])
def delete_stream(business_id):
    biz = get_business(business_id)
    if biz:
        idx = int(request.form.get("idx",-1))
        if 0 <= idx < len(biz["revenue_streams"]):
            biz["revenue_streams"].pop(idx)
            save_business(biz)
            flash("Stream removed.","success")
    return redirect(url_for("business_detail", business_id=business_id, tab="overview"))

# ── Setup progress: update ──────────────────────────────────────
@app.route("/business/<business_id>/progress/update", methods=["POST"])
def update_progress(business_id):
    biz = get_business(business_id)
    if biz:
        idx = int(request.form.get("idx",-1))
        if 0 <= idx < len(biz["setup_progress"]):
            pct = max(0, min(100, int(request.form.get("pct",0))))
            biz["setup_progress"][idx]["pct"]    = pct
            biz["setup_progress"][idx]["status"] = (
                "Done" if pct==100 else "In progress" if pct>0 else "Not started"
            )
            save_business(biz)
            flash("Progress updated.","success")
    return redirect(url_for("business_detail", business_id=business_id, tab="overview"))

# ── Run ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, port=5000)
