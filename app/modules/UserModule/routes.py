from flask import jsonify, request, json, Blueprint

from app import db
from app.models.Schemas import UserSchema
from app.modules.UserModule.UserController import UserController

user_bp = Blueprint('user_bp', __name__)


@user_bp.route("/users", methods=['GET'])
def routes():
    if request.method == 'POST':
        print("is in POST")
        return create_item()
    else:
        print("is in GET")
        return get_items()


@user_bp.route("/users/<int:user_id>", methods=['GET', 'PUT', 'DELETE'])
def item_details(user_id):
    # user_id = request.args.get('user_id')  # also can use for capture request GET param
    if request.method == 'GET':
        return get_item_details(user_id)
    elif request.method == 'PUT':
        return update_item(user_id)
    elif request.method == 'DELETE':
        return delete_item(user_id)
    response = {
        'status': 'error',
        'message': 'bad request body'
    }
    return jsonify(response), 400


def get_items():
    user_schema = UserSchema(many=True)  # many=True is to get many object
    users_list = UserController.get_items()
    if users_list is None:
        response = {
            'message': 'no user created'
        }
        return jsonify(response), 404
    result = user_schema.dump(users_list)
    # user_json = json.loads(result)  # load back as json object so the response won't treat it as db.String and escape it
    response = {
        'data_response': result,
    }
    return jsonify(response), 200


#  not gonna use for frontend as it suppose to get from db
def create_item():
    data = request.get_json()
    if 'username' in data and 'user_full_name' in data and 'user_email' in data:
        existing_user = UserController.find_user_by_username(username=data['username']).first()
        if existing_user is not None:
            response = {
                'message': 'user already exists'
            }
            return jsonify(response), 403
        error = UserController.create_item(username=data['username'], user_full_name=data['user_full_name'],
                                           user_email=data['user_email'])
        if type(error) is str:
            response = {
                'status': 'error',
                'message': error
            }
            return jsonify(response), 400
        response = {
            'message': "new user registered"
        }
        return jsonify(response), 202
    response = {
        'status': 'error',
        'message': 'bad request body'
    }
    return jsonify(response), 400


def get_item_details(user_id):
    user_schema = UserSchema()
    user = UserController.find_by_id(user_id)
    if user is None:
        response = {
            'message': 'user does not exist'
        }
        return jsonify(response), 404
    result = user_schema.dump(user)
    # user_json = json.loads(result)  # load back as json object so the response won't treat it as db.String and escape it
    response = {
        'data_response': result,
    }
    return jsonify(response), 200


def update_item(user_id):
    data = request.get_json()
    if 'user_role' in data and 'user_handle_industry' in data:
        user = UserController.find_by_id(user_id)
        # print(user)
        user.user_role_id = data['user_role']
        user.user_handle_industry_id = data['user_handle_industry']

        error = user.commit()
        if type(error) is str:
            response = {
                'message': error
            }
            return jsonify(response), 400
        response = {
            'message': 'user updated'
        }
        return jsonify(response), 202
    response = {
        'status': 'error',
        'message': 'bad request body'
    }
    return jsonify(response), 400


def delete_item(user_id):
    user = UserController.find_by_id(user_id)
    error = user.delete()
    if type(error) is str:
        response = {
            'status': 'error',
            'message': error
        }
        return jsonify(response), 400
    response = {
        'message': 'user deleted'
    }
    return jsonify(response), 202
