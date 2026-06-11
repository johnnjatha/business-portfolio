import os, sys
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from utils.data_loader import (
    load_businesses, get_business, save_business, add_business,
    delete_business_record, load_revenue, save_revenue_entry,
    delete_revenue_entry, revenue_summary, portfolio_summary
)

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "arstern-portfolio-2024"

@app.context_processor
def inject_globals():
    return dict(businesses=load_businesses(), enumerate=enumerate)

@app.route("/")
def index():
    return render_template("index.html", summary=portfolio_summary())

@app.route("/business/<business_id>")
def business_detail(business_id):
    biz = get_business(business_id)
    if not biz:
        flash("Business not found.", "error")
        return redirect(url_for("index"))
    return render_template("business_detail.html",
                           biz=biz, rev=revenue_summary(business_id),
                           tab=request.args.get("tab","overview"))

@app.route("/business/<business_id>/plan")
def business_plan(business_id):
    biz = get_business(business_id)
    if not biz: return redirect(url_for("index"))
    return render_template("business_plan.html", biz=biz)

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
        add_business(biz)
        flash(f"{name} added to your portfolio.","success")
        return redirect(url_for("business_detail", business_id=slug))
    return render_template("add_business.html")

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

@app.route("/business/<business_id>/delete", methods=["POST"])
def delete_business(business_id):
    biz = get_business(business_id)
    name = biz["name"] if biz else business_id
    delete_business_record(business_id)
    flash(f"{name} removed from your portfolio.","success")
    return redirect(url_for("index"))

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

@app.route("/business/<business_id>/revenue/delete", methods=["POST"])
def delete_revenue(business_id):
    f = request.form
    if f.get("year") and f.get("month"):
        delete_revenue_entry(business_id, int(f["year"]), int(f["month"]))
        flash("Entry deleted.","success")
    return redirect(url_for("business_detail", business_id=business_id, tab="revenue"))

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

if __name__ == "__main__":
    app.run(debug=True, port=5000)
