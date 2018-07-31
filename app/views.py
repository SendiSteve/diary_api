from flask_restful import Resource, reqparse
from flask import jsonify, make_response

from dbconnection import Connection
import re
from app.models import User

connection = Connection('postgres://admin:admin@localhost:5432/diary_db')


class RegisterResource(Resource):
    """ Defines endpoints for method calls for a user
        methods: GET, POST
        url: /api/auth/register
        url: /api/auth/login
     """

    def post(self):
        """Handles registration of a new user"""
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)

        args = parser.parse_args()
        username = args['username']
        email = args['email']
        password = args['password']

        email_exists = User.email_exists(email)

        if not re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)", email):
            return make_response(jsonify({'message': 'Please enter a valid email.'}), 400)

        if username.strip() == '' or len(username.strip()) < 3:
            return make_response(jsonify({'message': 'Please enter a valid username.'}), 400)

        if password.strip() == '' or len(password.strip()) < 5:
            return make_response(jsonify({'message': 'Please enter a valid password.'}), 400)

        if not email_exists:
            User.create_user_account(username, email, password)
            return make_response(jsonify({'message': 'User successfully registered.'}), 201)

        return make_response(jsonify({'message': 'Email already taken.'}), 400)
