from datetime import datetime, timedelta
import re

from flask import jsonify, request, abort
import jwt


from api.__init__ import app, databases
from api.v1.models import Users, BucketList, Items

databases.create_all()


@app.route('/bucketlist/api/v1/auth/register', methods=['POST'])
def register():
    request.get_json(force=True)
    try:
        name = request.json['username']
        pass_word = request.json['password']
        if not name:
            response = jsonify({'Error': 'Username not given.'})
            return response
        elif not re.match("^[a-zA-Z0-9_]*$", name):
            response = jsonify({'Error': 'Username contains special characters'})
            return response
        elif len(pass_word) < 6:
            response = jsonify({'Error': 'Password is too short, it must be more than 6 characters'})
            return response
        else:
            res = Users.query.all()
            name_check = [r.username for r in res]
            if name in name_check:
                response = jsonify({'Error': 'The Username already taken, register another name.'})
                return response
            else:
                user_data = Users(username=name)
                user_data.hash_password(pass_word)
                user_data.save()
                response = jsonify(
                    {'Registration status': user_data.username + 'successfully registered!!'})
                response.status_code = 201
                return response
    except KeyError:
        response = jsonify({
            'Error': 'Please use username and password for dict keys.'
        })
        response.status_code = 500
        return response


@app.route('/bucketlist/api/v1/auth/login', methods=['POST'])
def login():
    request.get_json(force=True)
    try:
        name = request.json['username']
        pass_word = request.json['password']
        res = Users.query.filter_by(username=name)
        user_name_check = [user.username for user in res if user.verify_password(pass_word) is True]
        user_id = [user.id for user in res if name in user_name_check]
        if not name:
            response = jsonify({'error': 'Username field cannot be blank'})
            response.status_code = 400
            return response
        elif not pass_word:
            response = jsonify({'error': 'Password field cannot be blank'})
            response.status_code = 400
            return response
        elif not re.match("^[a-zA-Z0-9_]*$", name):
            response = jsonify({'error': 'Username cannot contain special characters'})
            response.status_code = 400
            return response
        elif name in user_name_check:
            payload = {"user_id": user_id, "exp": datetime.utcnow() + timedelta(minutes=60)}
            token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
            response = jsonify({'Login status': 'Successfully Logged in ', 'Token': token.decode('utf-8')})
            response.status_code = 200
            return response
        else:
            response = jsonify({'Login status': 'Invalid credentials'})
            response.status_code = 200
            return response
    except KeyError:
        response = jsonify({'error': 'Please use username and password for dict keys.'})
        response.status_code = 500
        return response


def verify_token(request):
    token = request.headers.get("Authorization")
    if not token:
        abort(401)
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'],
                             algorithm='HS256')
    except jwt.ExpiredSignatureError:
        return jsonify({'Warning': 'Token is expired!'})
    except jwt.InvalidTokenError:
        response = jsonify({'error': 'Token is invalid'})
        response.status_code = 401
        return response
    return payload









































