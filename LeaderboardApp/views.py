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
                return confirmation(message=f"Votre défi {form['liste']} a bien été enregistré")
            except IntegrityError :
                return erreur_intégrité(message="Ce défi a déjà été enregistré")

#Création d'un défi
@app.route("/form/newdefi",methods=["GET","POST"])
def create_defi():
    if request.method == 'GET' :
        return render_template("create_defi.html")
    if request.method == 'POST' :
        form = request.form
        défi_name = form['name']
        coef = form['coef']
        try :
            solo = form['solo']
        except :
            solo = 0
        
        with Client() as client :
            try :
                client.createDéfis(défi_name,coef,solo)
                return confirmation(message=f"Votre défi {défi_name} a bien été enregistré")
            except IntegrityError :
                return erreur_intégrité(message="Ce défi existe déjà")

#Publication d'un défi solo
@app.route("/form/defisolo",methods=["GET","POST"])
def defisolo_page():
    if request.method == 'GET' :
        with Client() as client :
            team_name_list = [i[0] for i in client.get_table('teams','name')]
            defi_name_list = [i[0] for i in client.get_table('défis','name')]
              
        return render_template("add_defisolo.html",team_name_list=team_name_list,defi_name_list=defi_name_list)
    
    if request.method == 'POST' :
        form = request.form
        team_name = form['liste_equipe']
        défi_name = form['liste_defi']
        points = form['points']
        
        #Si un des champs est vide :
        if team_name=="" or défi_name =="" :
            return erreur_intégrité(message="Merci de remplir tout les champs")

        with Client() as client :
            try :
                new_id = 1 + client.get_max_id('défisolo')
                client.createDéfiSolo(new_id,défi_name,team_name,points)

                return confirmation(message=f"Le score de {points} points dans le défi \"{défi_name}\" de votre équipe {team_name} a bien été enregistré")
            except IntegrityError as e:
                print(e)
                return erreur_intégrité(message="Erreur de développement")

#Publication d'un défi vs
@app.route("/form/defivs",methods=["GET","POST"])
def defivs_page():
    if request.method == 'GET' :
        with Client() as client :
            team_name_list = [i[0] for i in client.get_table('teams','name')]
            defi_name_list = [i[0] for i in client.get_table('défis','name')]
              
        return render_template("add_defivs.html",team_name_list=team_name_list,defi_name_list=defi_name_list)
    
    if request.method == 'POST' :
        form = request.form
        team1_name = form['liste_equipe1']
        team2_name = form['liste_equipe2']
        défi_name = form['liste_defi']
        try :
            victoire1 = form['vequipe1']
        except :
            victoire1 = 0
        
        win_team = team1_name if victoire1 else team2_name
        
        #Si un des champs est vide :
        if team1_name=="" or team2_name=="" or défi_name =="" :
            return erreur_intégrité(message="Merci de remplir tout les champs")
        if team1_name == team2_name :
            return erreur_intégrité(message="Merci de saisir deux équipes différentes")

        with Client() as client :
            try :
                new_id = 1 + client.get_max_id('défivs')
                client.createDéfiVs(new_id,défi_name,team1_name,team2_name,victoire1)
                return confirmation(message=f"La victoire de {win_team} points dans le défi \"{défi_name}\" sur l'équipe {team2_name} a bien été enregistré")
            except IntegrityError as e:
                print(e)
                return erreur_intégrité(message="Erreur d'intégrité'")
#--------------------------------------------------------------


#Redirection page confirmation :
def confirmation(message:str):
    return render_template("confirmation.html",message=message)
def erreur_intégrité(message):
    return render_template("erreur_integrite.html",message=message)

#Services
def get_dict_leaderboard()->dict :
    return {} #TODO


