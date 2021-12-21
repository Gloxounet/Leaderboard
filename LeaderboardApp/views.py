from flask import Flask, request, render_template
from LeaderboardApp import app

from LeaderboardApp.models.sqlclient import Client
from LeaderboardApp.models.sqlclient import Error,IntegrityError



#Leaderboard--------------------------------------------------------------
@app.route("/")
def main_page():
    dict_leaderboard:dict = get_dict_leaderboard()
    return render_template("index.html",dict_leaderboard=dict_leaderboard)


#Formulaire---------------------------------------------------------------
@app.route("/form")
def form_page():
    return render_template("form_selection.html")


#Inscription Equipe
@app.route("/form/register",methods=["GET","POST"])
def register_page():
    if request.method == 'GET' :
        return render_template("register.html")
    if request.method == 'POST' :
        form = request.form
        
        with Client() as client :
            try :
                client.createTeam(form['name'])
                return confirmation(message=f"Votre équipe {form['name']} a bien été inscrite")
            except IntegrityError :
                return erreur_intégrité(message="Cette équipe est déjà enregistrée")

#Desinscription équipe
@app.route("/form/unregister",methods=["GET","POST"])
def unregister_page():
    if request.method == 'GET' :
        with Client() as client :
            team_name_list = [i[0] for i in client.get_table('teams','name')]    
        return render_template("unregister.html",name_list=team_name_list)
    
    if request.method == 'POST' :
        form = request.form
        with Client() as client :
            try :
                client.deleteTeam(form['liste'])
                return confirmation(message=f"Votre équipe {form['liste']} a bien été désinscrite")
            except IntegrityError :
                return erreur_intégrité(message="Cette équipe n'existe pas")


#Mise en ligne d'un défi solo
@app.route("/form/defisolo")
def defisolo_page():
    return "Building"


#Mise en ligne d'un défi vs
@app.route("/form/defivs")
def defivs_page():
    return "Building"
#--------------------------------------------------------------


#Redirection page confirmation :
def confirmation(message:str):
    return render_template("confirmation.html",message=message)
def erreur_intégrité(message):
    return render_template("erreur_integrite.html",message=message)

#Services
def get_dict_leaderboard()->dict :
    return {} #TODO


