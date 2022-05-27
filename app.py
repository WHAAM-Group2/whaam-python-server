from http import client
from flask import Flask, request
from flask_cors import CORS
from pymongo import MongoClient

"""
    A script that connects to a MongoDB instance and acts as an API for the
    connected web applications. The API will collect information from the databae 
    and return it to the web application. Alternatively, the API can be used to
    update the database configuration document with new information of a new player. 
"""

app = Flask(__name__)
CORS(app)


client = MongoClient(
    'mongodb://localhost:27017'
)

@app.route("/api/start_game", methods=["POST"])
def start_game():

    # Attempts to start a game by editing the configuration document in the database
    # with the username of the player who started the game.

    db = client.get_database("configuration")
    collection = db.get_collection("setup")

    collection.find_one_and_update(
        {"name": "setup"}, {"$set": {"username": request.json["username"],
                                     "status": True}})

    return {"status": True}

@app.route("/api/get_game_status", methods=["POST"])
def get_game_status():

    # Attempts to get the player status by reading the configuration 
    # document of that specific player. Will also return the latest 
    # game status of the player.

    db = client.get_database("configuration")
    collection = db.get_collection("players")

    doc = collection.find_one({"username": request.json["username"]})

    if doc is None:
        collection.insert_one({"username": request.json["username"],
                                 "status": "not playing"})
    
    doc = collection.find_one({"username": request.json["username"]})

    return {"status": doc["status"]}

@app.route("/api/get_game_ready_status")
def get_game_ready_status():

    # Attempts to get the status of the game by reading the configuration document.

    db = client.get_database("configuration")
    collection = db.get_collection("setup")

    doc = collection.find_one({"name": "setup"}, {"_id": 0})

    return {"status": doc}

@app.route("/api/get_scoreboard")
def get_scoreboard():

    # Collects information of previous games played, sorts them by score and returns
    # the top 10 scores.

    db = client.get_database("stats")
    collection = db.get_collection("scoreboard")

    docs = []

    for doc in collection.find({}, {"_id": 0}).sort("score", 1).limit(10):
        docs.append(doc)

    return {"games": docs}


# Run the application.

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
