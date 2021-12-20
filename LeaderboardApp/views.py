from flask import Flask, request, render_template
from LeaderboardApp import app

from LeaderboardApp.models.sqlclient import Client




@app.route("/")
def main_page():
    dict_leaderboard:dict = get_dict_leaderboard()
    return render_template("index.html",dict_leaderboard=dict_leaderboard)


###Formulaire################################################################
@app.route("/form")
def form_page():
    return render_template("form_selection.html")


#Inscription Equipe
@app.route("/form/register",methods=["GET","POST"])
def register_page():
    if request.method == 'GET' :
        return render_template("register.html")

@app.route("/form/register/done",methods=["GET","POST"])
def inscription_confirmation() :
    pass

#Desinscription équipe
@app.route("/form/unregister")
def unregister_page():
    return "Building"


#Mise en ligne d'un défi solo
@app.route("/form/defisolo")
def defisolo_page():
    return "Building"


#Mise en ligne d'un défi vs
@app.route("/form/defivs")
def defivs_page():
    return "Building"
#################################################################################




#Services
def get_dict_leaderboard()->dict :
    return {} #TODO


