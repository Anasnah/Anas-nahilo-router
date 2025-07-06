from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)
app.secret_key = "anas2000nahilo"
DATA_FILE = "tickets.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/devices")
def devices():
    now = datetime.now()
    devices = [d for d in load_data() if "mac" in d and datetime.strptime(d["end_date"], "%Y-%m-%d") > now]
    return render_template("index.html", devices=devices)

@app.route("/add_device", methods=["GET", "POST"])
def add_device():
    if not session.get("admin"):
        return redirect(url_for("admin"))

    if request.method == "POST":
        device_name = request.form["device_name"]
        mac = request.form["mac"]
        duration_days = int(request.form["duration"])
        start_date = datetime.now()
        end_date = start_date + timedelta(days=duration_days)

        ticket = {
            "device_name": device_name,
            "mac": mac,
            "duration": duration_days,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }

        data = load_data()
        data.append(ticket)
        save_data(data)

        flash("تمت إضافة تذكرة الحظر بنجاح!", "success")
        return redirect(url_for("devices"))

    return render_template("add_device.html")

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        if request.form.get("password") == "anas2000nahilo":
            session["admin"] = True
            return redirect(url_for("add_device"))
        else:
            flash("كلمة المرور غير صحيحة", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("devices"))

if __name__ == "__main__":
    app.run(debug=True)
