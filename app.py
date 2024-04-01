from flask import Flask
from flask import request, render_template
import datetime
from flask import Markup
import sqlite3

app = Flask(__name__)

from flask import redirect
from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

dashboard = Dash(__name__, server=app, url_base_pathname="/dash/", external_stylesheets=[dbc.themes.CYBORG])
dashboard.layout = html.Div(
        [
            html.Div(id='live-update-text'),
            dcc.Interval(id='interval-component')
        ],
        style={"display":"flex", "justify-content": "center", "align-items": "center"}
        )

@app.route('/dashboard',methods=["GET","POST"]) 
def dashboard():
    print("d0")
    return redirect('/dash')

@callback(Output('live-update-text', 'children'),
          Input('interval-component', 'n_intervals'))
def update_metrics(n):
    print("d2")
    
    conn = sqlite3.connect('log.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM user")
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    
    return [
        dbc.Card(
            dbc.CardBody([
                 html.H2("Name Count {0}".format(count)),
            ]),
        ),        
        html.Br(),
        dbc.Button(
            "Go Back", id="back", className="back", external_link=True, href="/main",
        ),
    ]

name = ""
flag = 1

@app.route("/", methods = ["GET", "POST"])
def index():
    return(render_template("index.html"))

@app.route("/main", methods = ["GET", "POST"])
def main():
    global flag, name
    if flag == 1:
        name = request.form.get("q")
        flag = 0
    currentDateTime = datetime.datetime.now()
    conn = sqlite3.connect('log.db')
    c = conn.cursor()
    c.execute('INSERT INTO user (name,timestamp) VALUES(?,?)',(name,currentDateTime))
    conn.commit()
    c.close()
    conn.close()
    return(render_template("main.html", r = name))
           
@app.route("/prediction", methods = ["GET", "POST"])
def prediction():
    return(render_template("prediction.html"))

def prediction():
    return(render_template("prediction.html"))
           
@app.route("/result", methods = ["GET", "POST"])
def result():
    q = float(request.form.get("q"))
    return(render_template("result.html", r = 90.2-(50.6*q)))

@app.route("/query", methods = ["GET", "POST"])
def query():
    conn = sqlite3.connect('log.db')
    #c = conn.cursor()
    r = ""
    for row in conn.execute("select * from user"):
        print(row)
        r = r + str(row) + "<br>"
        print(r)
    #c.close()
    conn.close
    r = Markup(r)
    return(render_template("query.html",r=r))

@app.route("/delete", methods = ["GET", "POST"])
def delete():
    conn = sqlite3.connect('log.db')
    c = conn.cursor()
    c.execute('DELETE FROM user;',);
    conn.commit()
    c.close()
    conn.close()  
    return(render_template("delete.html"))

@app.route("/end", methods = ["GET", "POST"])
def end():
    global flag
    print("handling of ending......")
    flag = 1
    return(render_template("index.html"))

if __name__=="__main__":
    app.run()
