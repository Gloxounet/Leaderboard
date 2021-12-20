#Load up the app
from LeaderboardApp import app;

# Launching our server
if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")