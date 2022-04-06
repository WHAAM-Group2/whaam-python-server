from flask import Flask
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


# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
