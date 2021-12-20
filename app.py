from flask import Flask, request, render_template

app = Flask(__name__)


@app.route("/")
def main_page():
    dict_leaderboard:dict = get_dict_leaderboard()
    return render_template("index.html",dict_leaderboard=dict_leaderboard)

@app.route("/form")
def form_page():
    return render_template("form_selection.html")

@app.route("/form/register",methods=["GET","POST"])
def register_page():
    if request.method == 'GET' :
        return render_template("register.html")

@app.route("/form/register/done",methods=["GET","POST"])
def inscription_confirmation():
    print(f"Inscription équipe {request.form['name']}")#TODO SQL INSCRIPTION
    return render_template('confirmation.html',team_name=f"Votre équipe {request.form['name']} a bien été enregistrée")

@app.route("/form/unregister")
def unregister_page():
    return "Building"

@app.route("/form/defisolo")
def defisolo_page():
    return "Building"

@app.route("/form/defivs")
def defivs_page():
    return "Building"





#Services
def get_dict_leaderboard()->dict :
    return {}


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")