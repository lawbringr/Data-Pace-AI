from config import client
from app import app
from bson.json_util import dumps
from flask import request, jsonify
import json
import ast
import imp


# helpers module
helper_module = imp.load_source('*', './app/helpers.py')

# db
db = client.assignment
# collection
collection = db.users

@app.route("/")
def get_initial_response():
    """DATA PACE AI TECHNOLOGIES ASSIGNMENT"""
    message = {
        'apiVersion': 'v1.0',
        'status': '200',
        'message': 'Internship Assignment'
    }
    resp = jsonify(message)
    return resp

@app.route("/api/users", methods=['GET'])
def fetch_users():
    """fetch the users using query
       """
    try:
        query_params = helper_module.parse_query_params(request.query_string)
        if query_params:
            query = {k: int(v) if isinstance(v, str) and v.isdigit() else v for k, v in query_params.items()}            
            
            page = 1
            
            if 'page' in query:
                page = int(query['page'])
            
            if 'limit' not in query:
                query['limit'] = 5
            
            sort_order = 1
            sort_param = 'id'
            
            if 'sort' in query:
                if query['sort'][0] == '-':
                    sort_order = -1
                    sort_param = query['sort'][1:]
                else:
                    sort_param = query['sort']
 
            regex_q = {
                "$regex": query['name'],
                "$options" :'i' # case-insensitive
            }
            
            user_query = {"first_name":regex_q}
            records_fetched = collection.find(user_query).sort(sort_param, sort_order).skip((page-1)*query['limit']).limit(query['limit'])

            if records_fetched.count() > 0:
                return dumps(records_fetched), 200
            else:
                del user_query['first_name']
                user_query['last_name'] = regex_q
                records_fetched = collection.find(user_query).sort(sort_param, sort_order).skip((page-1)*query['limit']).limit(query['limit'])

            if records_fetched.count() > 0:
                return dumps(records_fetched), 200
            else:
                return "User not found using query parameters", 404

        else:
            if collection.find().count > 0:
                return dumps(collection.find())
            else:
                return jsonify([])
    except:
        return "", 500

@app.route("/api/users", methods=['POST'])
def create_user():
    """create new users
       """
    try:
        try:
            body = ast.literal_eval(json.dumps(request.get_json()))
        except:
            print "Request body not found"
            return ""

        record_created = collection.insert(body)

        if isinstance(record_created, list):
            return jsonify([str(v) for v in record_created]), 201
        else:
            return jsonify(str(record_created)), 201
    except:
        return "", 500

@app.route("/api/users/<user_id>", methods=['GET'])
def fetch_user(user_id):
    """get details of the user using ID.
       """
    try:
        records_fetched = collection.find({"id": int(user_id)})

        if records_fetched.count() > 0:
            return dumps(records_fetched), 200
        else:
            return "Can't find user", 404
    except:
        return "", 500

@app.route("/api/users/<user_id>", methods=['PUT'])
def update_user(user_id):
    """update the user.
       """
    try:
        try:
            body = ast.literal_eval(json.dumps(request.get_json()))
        except:
            return "Body Not available"

        records_updated = collection.update_one({"id": int(user_id)}, body)

        if records_updated.modified_count > 0:
            return "", 200
        else:
            return "Not Updated", 404
    except:
        return "", 500


@app.route("/api/users/<user_id>", methods=['DELETE'])
def remove_user(user_id):
    """remove the user.
       """
    try:
        delete_user = collection.delete_one({"id": int(user_id)})

        if delete_user.deleted_count > 0 :
            return "", 200
        else:
            return "Unable to find user", 404
    except:
        return "", 500


@app.errorhandler(404)
def page_not_found(e):
    """Send message to the user with notFound 404 status."""
    message = {
        "err":
            {
                "msg": "This route is not supported"
            }
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp
