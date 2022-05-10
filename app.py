from http import client
from flask import Flask, request
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# client = MongoClient(
#     'mongodb+srv://whaam:B-oop123@project2022.yskak.mongodb.net/myFirstDatabase?retryWrites=true&w=majority&tls=true&tlsAllowInvalidCertificates=true')

client = MongoClient(
    'mongodb://localhost:27017'
)

# Registers a new user


@app.route("/api/start_game", methods=["POST"])
def start_game():

    db = client.get_database("configuration")
    collection = db.get_collection("setup")

    collection.find_one_and_update(
        {"name": "setup"}, {"$set": {"username": request.json["username"],
                                     "status": True}})

    return {"status": True}

# Shows player status


@app.route("/api/get_game_status", methods=["POST"])
def get_game_status():

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
    db = client.get_database("configuration")
    collection = db.get_collection("setup")

    doc = collection.find_one({"name": "setup"}, {"_id": 0})

    return {"status": doc}


# Showing the game scoreboard


@app.route("/api/get_scoreboard")
def get_scoreboard():

    db = client.get_database("stats")
    collection = db.get_collection("scoreboard")

    docs = []

    for doc in collection.find({}, {"_id": 0}).sort("score", 1).limit(10):
        docs.append(doc)

    return {"games": docs}


# Run the app


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
