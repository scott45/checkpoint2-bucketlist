from datetime import datetime, timedelta
import re

from flask import jsonify, request, abort
import jwt


from api.__init__ import app, databases
from api.v1.models import Users

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
