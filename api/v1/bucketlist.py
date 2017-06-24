# import modules, models and configs
from datetime import datetime, timedelta
import re

import jwt
from flask import jsonify, request, abort

from api.__init__ import app, databases
from api.v1.models import Users, BucketList, Items

databases.create_all()


# 404 error handler
@app.errorhandler(404)
def page_not_found():
    response = jsonify({'error': 'The request can not be linked to, Please check your endpoint url'})
    response.status_code = 404
    return response


# 405 error handler
@app.errorhandler(405)
def method_not_allowed(e):
    response = jsonify({'error': 'Invalid request method. Please check your the request method being used'})
    response.status_code = 405
    return response


# user registration method
@app.route('/bucketlist/api/v1/auth/register', methods=['POST'])
def register():
    request.get_json(force=True)
    try:
        name = request.json['username']
        pass_word = request.json['password']

        if not name and not pass_word:
            response = jsonify({'error': 'Username and password field cannot be blank'})
            response.status_code = 400
            return response

        if len(pass_word) < 6:
            response = jsonify({'Error': 'Password is too short, it must be more than 6 characters'})
            response.status_code = 401
            return response

        if not re.match("^[a-zA-Z0-9_]*$", name):
            response = jsonify({'error': 'Username cannot contain special characters'})
            response.status_code = 401
            return response

        res = Users.query.all()
        name_check = [r.username for r in res]
        if name in name_check:
            response = jsonify({'Error': 'The Username already taken, register another name.'})
            response.status_code = 401
            return response
        else:
            user_data = Users(username=name)
            user_data.hash_password(pass_word)
            user_data.save()
            response = jsonify(
                {'Registration status': user_data.username + ' successfully registered!!'})
            response.status_code = 201
            return response
    except KeyError:
        response = jsonify({
            'Error': 'Please use username and password for dict keys and ensure accurate urls.'
        })
        response.status_code = 500
        return response


# user login method
@app.route('/bucketlist/api/v1/auth/login', methods=['POST'])
def login():
    request.get_json(force=True)
    try:
        name = request.json['username']
        pass_word = request.json['password']

        if not name and not pass_word:
            response = jsonify({'error': 'Username and password field cannot be blank'})
            response.status_code = 400
            return response

        elif not re.match("^[a-zA-Z0-9_]*$", name):
            response = jsonify({'error': 'Username cannot contain special characters'})
            response.status_code = 400
            return response

        res = Users.query.all()
        user_name_check = [user.username for user in res if user.verify_password(pass_word) is True]
        user_id = [user.id for user in res if name in user_name_check]

        if name in user_name_check:
            payload = {"user_id": user_id, "exp": datetime.utcnow() + timedelta(minutes=60)}
            token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
            response = jsonify({'Login status': 'Login successful', 'Token': token.decode('utf-8')})
            return response
        else:
            response = jsonify({'Login status': 'Invalid credentials'})
            response.status_code = 401
            return response
    except KeyError:
        response = jsonify({'error': 'Please use username and password for dict keys and ensure accurate urls.'})
        response.status_code = 500
        return response


# verify token method
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


# add bucket method
@app.route('/bucketlist/api/v1/bucketlist', methods=['POST'])
def add_bucket():
    request.get_json(force=True)
    try:
        verification = verify_token(request)
        if isinstance(verification, dict):
            user_id = verification['user_id']
        else:
            return verification
        b_name = request.json['name']
        if not b_name:
            response = jsonify({'Error': 'bucketlist has no name'})
            response.status_code = 403
            return response
        else:
            b = BucketList(name=b_name, created_by=user_id[0])
            b.save()
            response = jsonify({'status': 'Bucket added successfully'})
            response.status_code = 201
            return response
    except KeyError:
        response = jsonify({'Error': 'Use the name for dict key.'})
        response.status_code = 500
        return response


# get bucket method
@app.route('/bucketlist/api/v1/bucketlist', methods=['GET'])
def retrieve_bucketlist():
    message = 'No bucketlists have been created'
    payload = verify_token(request)
    if isinstance(payload, dict):
        user_id = payload['user_id']
    else:
        return payload
    respons = BucketList.query.all()
    if not respons:
        response = jsonify({'error': 'No bucketlists have been created'})
        response.status_code = 200
        return response
    else:
        limit = int(request.args.get("limit", 20))
        if limit > 100:
            limit = 100
        search = request.args.get("q", "")
        if search:
            res = [bucket for bucket in respons if bucket.name in search and bucket.created_by in user_id]
            if not res:
                response = jsonify({'error': message})
                response.status_code = 200
                return response
            else:
                bucketlist_data = []
                for data in res:
                    final = {
                        'id': data.id,
                        'name': data.name,
                        'date-created': data.date_created,
                        'date_modified': data.date_modified,
                        'created_by': data.created_by,
                    }
                    bucketlist_data.clear()
                    bucketlist_data.append(final)
                response = jsonify(bucketlist_data)
                response.status_code = 200
                return response
        else:
            res = [bucket for bucket in respons if bucket.created_by in user_id]
            bucketlist_data = []
            if not res:
                response = jsonify({'error': message})
                response.status_code = 200
                return response
            else:
                for data in res:
                    final = {
                        'id': data.id,
                        'name': data.name,
                        'date-created': data.date_created,
                        'date_modified': data.date_modified,
                        'created_by': data.created_by,
                    }
                    bucketlist_data.append(final)
                response = jsonify(bucketlist_data)
                response.status_code = 200
                return response


# get, update and delete bucket method
@app.route('/bucketlist/api/v1/bucketlist/<int:bucket_id>', methods=['GET', 'PUT', 'DELETE'])
def bucket_by_id(bucket_id):
    payload = verify_token(request)
    if isinstance(payload, dict):
        user_id = payload['user_id']
    else:
        return payload
    res = BucketList.query.all()
    bucket_data = [bucket for bucket in res if bucket.id == bucket_id and bucket.created_by in user_id]
    if request.method == 'GET':
        data = {}
        for data in bucket_data:
            final_data = []
            for item_data in bucket_data:
                item_data = {
                    'id': item_data.id,
                    'name': item_data.name,
                    'date-created': item_data.date_created,
                    'date_modified': item_data.date_modified,
                }
                final_data.append(item_data)
            data = {
                'id': data.id,
                'name': data.name,
                'date-created': data.date_created,
                'date_modified': data.date_modified,
                'items': final_data
            }
        if bucket_id not in data.values():
            response = jsonify({'warning': 'the bucketlist does not exist.'})
            response.status_code = 404
            return response
        else:
            response = jsonify(data)
            response.status_code = 200
            return response
    elif request.method == 'DELETE':
        data = {}
        for data in bucket_data:
            data = {
                'id': data.id,
                'name': data.name,
                'date-created': data.date_created,
                'date_modified': data.date_modified
            }
        if bucket_id not in data.values():
            response = jsonify({'warning': 'the bucketlist does not exist.'})
            response.status_code = 404
            return response
        else:
            delete = BucketList.query.filter_by(id=bucket_id).first()
            databases.session.delete(delete)
            databases.session.commit()
            response = jsonify({'Status': 'Bucketlist deleted successfully.'})
            response.status_code = 200
            return response
    elif request.method == 'PUT':
        request.get_json(force=True)
        data = BucketList.query.filter_by(id=bucket_id).first()
        if not data:
            response = jsonify({'warning': 'the bucketlist does not exist.'})
            response.status_code = 404
            return response
        else:
            try:
                name = request.json['name']
                data.name = name
                databases.session.commit()
                data = {}
                for data in bucket_data:
                    data = {
                        'id': data.id,
                        'name': data.name,
                        'date-created': data.date_created,
                        'date_modified': data.date_modified
                    }
                response = jsonify(data)
                response.status_code = 201
                return response
            except KeyError:
                response = jsonify({'error': 'Please use name for dict keys.'})
                response.status_code = 500
                return response


# add bucket item method
@app.route('/bucketlist/api/v1/bucketlist/<int:bucket_id>/items', methods=['POST'])
def add_items(bucket_id):
    payload = verify_token(request)
    if isinstance(payload, dict):
        user_id = payload['user_id']
    else:
        return payload
    respons = BucketList.query.all()
    resp = [data for data in respons if data.created_by in user_id and data.id == bucket_id]
    if not resp:
        response = jsonify({'Warning': 'The provided bucketlist_id does not exist.'})
        response.status_code = 404
        return response
    else:
        try:
            item_data = Items.query.all()
            request.get_json(force=True)
            item_name = request.json['name']
            item_check = [item.name for item in item_data if item.name == item_name]
            if item_check:
                response = jsonify({'Warning': 'this item already exists.'})
                return response
            else:
                item_add = Items(name=item_name, id=bucket_id)
                item_add.save()
                response = jsonify({'Status': 'Success, item has been created'})
                response.status_code = 200
                return response
        except KeyError:
            response = jsonify({'error': 'Please use name for dict keys.'})
            response.status_code = 500
            return response


# update bucket item method
@app.route('/bucketlist/api/v1/bucketlist/<int:bucket_id>/items/<int:item_id>', methods=['PUT'])
def edit_items(bucket_id, item_id):
    request.get_json(force=True)
    payload = verify_token(request)
    if isinstance(payload, dict):
        user_id = payload['user_id']
    else:
        return payload
    resp = BucketList.query.all()
    res = [data for data in resp if data.created_by in user_id and
           data.id == bucket_id]
    items_response = Items.query.filter_by(id=item_id).first()
    if not res:
        response = jsonify({'Warning': 'The bucketlist_id does not exist.'})
        response.status_code = 404
        return response
    elif not items_response:
        response = jsonify({'Warning': 'The item_id does not exist.'})
        response.status_code = 404
        return response
    else:
        try:
            new_name = request.json['name']
            items_response.name = new_name
            databases.session.commit()
            response = jsonify({'Status': 'Bucketlist Item successfully edited.'})
            response.status_code = 200
            return response
        except KeyError:
            response = jsonify({'error': 'Please use name for dict keys.'})
            response.status_code = 500
            return response


# delete bucket item method
@app.route('/bucketlist/api/v1/bucketlist/<int:bucket_id>/items/<int:item_id>', methods=['DELETE'])
def delete_item(bucket_id, item_id):
    payload = verify_token(request)
    if isinstance(payload, dict):
        user_id = payload['user_id']
    else:
        return payload
    res = BucketList.query.filter_by(id=bucket_id).first()
    items_response = Items.query.filter_by(id=item_id).first()
    if not res:
        response = jsonify({'Warning': 'The bucketlist_id does not exist.'})
        response.status_code = 404
        return response
    elif not items_response:
        response = jsonify({'Warning': 'The item_id does not exist.'})
        response.status_code = 404
        return response
    else:
        databases.session.delete(items_response)
        databases.session.commit()
        response = jsonify({'Status': 'Item deleted successfully.'})
        response.status_code = 200
        return response
