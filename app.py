from flask import Flask, request, redirect, render_template, session
import content_scrapers as cs
import datetime
import sqlite3 as db
import re as re

from org_class import Nonprofit

con = db.connect("nonprofits.db")
cur = con.cursor()
nonprofits_master = list(cur.execute("SELECT DISTINCT name FROM url;").fetchall())
con.close()

def scrape_bts(org):
    table = ["oops"]
    # if org in nonprofits_master:
    with db.connect("nonprofits.db") as con:
        cur = con.cursor()
        url = cur.execute("SELECT site, content FROM url WHERE name = '{}';".format(org)).fetchone()
    con.close()
    Partner = Nonprofit(org, url[0], url[1], cs.content_scraper[org])
    table = Partner.scrape_content().to_html(classes="data", header = "true", index = False)
    return table
    
################################ APP BEGINS HERE ################################

app = Flask(__name__)
app.secret_key = "penny"
# works in http://127.0.0.1:5000

@app.route("/", methods = ["GET", "POST"])
def scraper():
    if request.method == "POST": 
        session["nonprofits"] = request.form.get("orgs")
        return redirect("/scrape_results")
    return render_template(
        "scraper.html",
        all = nonprofits_master
    )

@app.route("/scrape_results")
def show_scrape_tables():
    nonprofits_list = re.split(",[ ]*", session["nonprofits"])
    tables = list()
    for org in nonprofits_list:
        table = scrape_bts(org)
        tables.append(table)
    return render_template(
        "scrape_results.html", 
        nonprofits = nonprofits_list, 
        length = len(session["nonprofits"]),
        tables = tables
    )

if __name__ == "__main__":
    app.config['SESSION_TYPE'] = 'filesystem'
    sess.init_app(app)
    app.run(debug = True)