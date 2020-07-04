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

@app.route("/api/v1/register", methods=['POST'])
def register():
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _password = _json['password']
    _passwordConfirm = _json['passwordConfirm']
    _phone = _json['phone']
    _msv = _json['msv']
    _role = _json['role']
    if _name and _email and _password and _passwordConfirm and _phone and _msv and _role and request.method == 'POST':
        query = collection.find_one({"email": _email})
        if(query):
            return jsonify({'message': 'Email đã tồn tại'})
        else:
            if(len(_password) < 8):
                return jsonify({'message': "Mật khẩu của bạn phải dài hơn 8 ký tự"})
            elif(_password != _passwordConfirm):
                return jsonify({'message': 'Mật khẩu nhập lại chưa khớp'})
            else:
                user = {
                    "name": _name,
                    "email": _email,
                    "password": generate_password_hash(_password),
                    "phone": _phone,
                    "msv": _msv,
                    "role": _role
                }
                queryInsert = collection.insert_one(user)
                if(queryInsert):
                    queryFindUserId = collection.find_one({"_id": queryInsert.inserted_id})
                    if(queryFindUserId):
                        return jsonify({'message':"Tạo tài khoản thành công", "data": dumps(queryFindUserId)})
                    else:
                        return jsonify({'message': 'Có lỗi xảy ra, vui lòng thử lại'})
                    
                else:
                    return jsonify({'message': 'Có lỗi xảy ra, vui lòng thử lại'})
    else:
        return jsonify({'message': 'Chưa nhập đủ thông tin'})
