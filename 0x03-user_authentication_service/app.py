#!/usr/bin/env python3
"""
app.py
"""
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def index():
    """
    starting up a flask app
    """
    payload = {"message": "Bienvenue"}
    return jsonify(payload)


@app.route("/users", methods=["POST"], strict_slashes=False)
def user():
    """
    this checkes for a user
    """
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        if not email or not password:
            return jsonify({"message": "Email and Password are required"}), 400
        AUTH.register_user(email=email, password=password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    from auth import Auth
    AUTH = Auth()
    app.run(host="0.0.0.0", port="5000")
