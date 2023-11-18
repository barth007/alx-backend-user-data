#!/usr/bin/env python3
"""
app.py
"""
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def index():
    """
    starting up a flask app
    """
    payload = {"message": "Bienvenue"}
    return jsonify(payload)

@app.route("/users/<email>/<password>", methods=["POST"], strict_slashes=False)
def user(email: str, password: str):
   



if __name__ == "__main__":
    from auth import Auth
    AUTH = Auth()
    app.run(host="0.0.0.0", port="5000")
