from flask import Flask, request, render_template

app = Flask(__name__)

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/")
def main_page():
    dict_leaderboard:dict = get_dict_leaderboard()
    return render_template("index.html",dict_leaderboard=dict_leaderboard)

@app.route("/form")
def form_page():
    return render_template("form_selection.html")

@app.route("/form/register")
def register_page():
    return "Building"

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
    app.run()