from config import *
from bson.json_util import dumps
from flask import request, jsonify, make_response
import json
import ast
from importlib.machinery import SourceFileLoader
from app import app
from bson.objectid import ObjectId
import jwt
import datetime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
db = client.restfulapi
collection = db.users

app.config['SECRET_KEY'] = 'lethanhdat'

def token_require(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Thiếu Token'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : 'Token chưa được valid'}), 403
        return f(*args, **kwargs)
    return decorated
    
@app.route("/api/v1/login", methods=['POST'])
def login():
    print("access login route")
    _json = request.json
    _email = _json['email']
    _password = _json['password']
    if _email and _password and request.method == 'POST':
        print(_email)
        query = collection.find_one({"email": _email})
        if(query):
            password = query['password']
            if check_password_hash(password, _password):
                token = jwt.encode({'user': _email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
                return jsonify({'token': token.decode('UTF-8')})
            else:
                return jsonify({'message': 'sai mật khẩu'})
        else:
            return jsonify({'message': 'Không tồn tại Email'})
    else:
        return not_found()
@app.errorhandler(404)
def not_found(error=None):
    message = {
        "status": 404,
        "err":"Xin nhập đầy đủ thông tin"
    }
    resp = jsonify(message)

    resp.status_code = 404

    return resp
