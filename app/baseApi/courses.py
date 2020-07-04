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
helper_module = SourceFileLoader('*', './app/helpers.py').load_module()

db = client.restfulapi
collection = db.courses

@app.route("/api/v1/courses", methods=['GET'])
def fetch_courses():
    try:
        query_params = helper_module.parse_query_params(request.query_string)
        if query_params:
            query = {k: int(v) if isinstance(v, str) and v.isdigit() else v for k, v in query_params.items()}
            records_fetched = collection.find(query)
            if records_fetched.count() > 0:
                return records_fetched.count
            else:
                return "", 404
        else:
            if collection.find().count() > 0:
                return dumps(collection.find())
            else:
                return jsonify([])
    except:
        return "", 500

@app.route("/api/v1/courses", methods=['POST'])
def create_course():
    _json = request.json
    _name = _json['name']
    _category = _json['category']
    _img = _json['img']
    _listCourse = _json['listCourse']
    if _name and _category and _img and _listCourse and request.method == 'POST':
        course = {
            "name": _name,
            "category": _category,
            "img": _img,
            "listCourse": _listCourse
        }
        queryInsert = collection.insert_one(course)
        if(queryInsert):
            return jsonify({'message':"Tạo thành công", "_id": dumps(queryInsert.inserted_id)})
        else:
            return jsonify({'message':"Đã có lỗi xảy ra vui lòng thử lại"})
    else:
        return jsonify({'message': 'Chưa nhập đủ thông tin'})