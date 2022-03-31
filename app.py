from flask import Flask

app = Flask(__name__)

@app.route("/misc")
def hello_world():
    return {"message": "Hello World!"}