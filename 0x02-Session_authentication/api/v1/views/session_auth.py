#!/usr/bin/env python3
""" Module of Session auth views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
import os


@app_views.route('/auth_session/login/',
                 methods=['POST'], strict_slashes=False)
@app_views.route('/auth_session/login',
                 methods=['POST'], strict_slashes=False)
def login_session():
    """
    creating a auth session for every login user
    """

    if request.method == 'POST':
        email = request.form.get('email')
        if email is None:
            return jsonify({"error": "email missing"}), 400
        password = request.form.get('password')
        if password is None:
            return jsonify({"error": "password missing"}), 400
        # searching if user exist
        users = User.search({'email': email})
        if users is None or not users:
            return jsonify({"error": "no user found for this email"}), 404
        user = users[0]
        if user.is_valid_password(password) is False:
            return jsonify({"error": "wrong password"}), 401
        # creating a Session
        from api.v1.app import auth
        session_id = auth.create_session(user.id)
        response = jsonify(user.to_json())
        # set cookie
        cookie_data = os.getenv("SESSION_NAME")
        response.set_cookie(cookie_data, session_id)
        return response


@app_views.route('/api/v1/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    """
    logout users out
    """

    if request.method == 'DELETE':
        from api.v1.app import auth
        status = auth.destroy_session(request)
        if not status:
            abort(404)
        else:
            return jsonify({}), 200
