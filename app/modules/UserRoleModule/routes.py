from flask import jsonify, request, json, Blueprint

from app import db
from app.models.Schemas import UserRoleSchema
from app.modules.UserRoleModule.UserRoleController import UserRoleController

user_role_bp = Blueprint('user_role_bp', __name__)


@user_role_bp.route("/roles", methods=['GET', 'POST'])
def roles():
    if request.method == 'POST':
        return create_role()
    else:
        return get_roles()


@user_role_bp.route("/roles/<int:item_id>", methods=['GET', 'PUT', 'DELETE'])
def role_details(item_id):
    # user_id = request.args.get('user_id')  # also can use for capture request GET param
    if request.method == 'GET':
        return get_role_details(item_id)
    elif request.method == 'PUT':
        return update_role(item_id)
    elif request.method == 'DELETE':
        return delete_role(item_id)
    response = {
        'status': 'error',
        'message': 'Bad request body.'
    }
    return jsonify(response), 400


def get_roles():
    role_schema = UserRoleSchema(many=True)
    role_list = UserRoleController.get_roles()
    if role_list is None:
        response = {
            'message': 'No role created.'
        }
        return jsonify(response), 404
    result = role_schema.dumps(role_list)
    json_response = json.loads(result)
    response = {
        'data_response': json_response,
    }
    return jsonify(response), 200


def create_role():
    data = request.get_json()
    if 'user_role_description' in data and 'user_role_json' in data:
        error = UserRoleController.create_role(data['user_role_description'], data['user_role_json'])
        if error is not None:
            response = {
                'status': 'error',
                'message': error
            }
            return jsonify(response), 400
        response = {
            'message': "New role registered."
        }
        return jsonify(response), 202
    response = {
        'status': 'error',
        'message': 'Bad request body.'
    }
    return jsonify(response), 400


def get_role_details(item_id):
    role_schema = UserRoleSchema()
    role = UserRoleController.find_role_by_id(item_id)
    if role is None:
        response = {
            'message': 'Role does not exist.'
        }
        return jsonify(response), 404
    result = role_schema.dumps(role)
    json_response = json.loads(
        result)  # load back as json object so the response won't treat it as db.String and escape it
    response = {
        'data_response': json_response,
    }
    return jsonify(response), 200


def update_role(item_id):
    data = request.get_json()
    if 'user_role_description' in data and 'user_role_json' in data:
        role = UserRoleController.find_role_by_id(item_id)
        # print(user)
        role.user_role_description = data['user_role_description']
        role.user_role_json = data['user_role_json']

        db.session.commit()
        response = {
            'message': 'Role updated.'
        }
        return jsonify(response), 202
    response = {
        'status': 'error',
        'message': 'Bad request body.'
    }
    return jsonify(response), 400


def delete_role(item_id):
    role = UserRoleController.find_role_by_id(item_id)
    error = role.delete()
    if error is not None:
        response = {
            'status': 'error',
            'message': error
        }
        return jsonify(response), 400
    response = {
        'message': 'Role deleted.'
    }
    return jsonify(response), 202
