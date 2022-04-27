from flask import Flask, request
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

client = MongoClient(
    'mongodb+srv://whaam:B-oop123@project2022.yskak.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')


@app.route("/api/server")
def hello_world():

    db = client.get_database("configuration")
    collection = db.get_collection("setup")

    doc = collection.find_one({"name": "setup"})
    print(doc)

    return {"status": doc["status"]}


@app.route("/api/get_movement")
def get_movement():

    db = client.get_database("configuration")
    collection = db.get_collection("setup")

    # collection.insert_one({"name": "movement", "status": ""})
    doc = collection.find_one({"name": "movement"})

    return {"status": doc["status"]}


@app.route("/api/start_game", methods=["POST"])
def start_game():

    db = client.get_database("configuration")
    collection = db.get_collection("setup")

    collection.find_one_and_update(
        {"name": "setup"}, {"$set": {"username": request.json["username"],
                                     "status": True}})

    # print(request.json["username"])

    return {"status": True}


@app.route("/api/games_played")
def games_played():

    db = client.get_database("stats")
    collection = db.get_collection("games")

    docs = []

    for doc in collection.find({}, {"_id": 0}).sort("score", 1).limit(5):
        docs.append(doc)

    return {"games": docs}


# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
