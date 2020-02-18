from flask import jsonify, request, json, Blueprint

from app import db
from app.models.Schemas import IndustryAreaSchema
from app.modules.IndustryAreaModule.IndustryAreaController import IndustryAreaController

industry_area_bp = Blueprint('industry_area_bp', __name__)


@industry_area_bp.route("/industry-areas", methods=['GET', 'POST'])
def routes():
    if request.method == 'POST':
        return create_item()
    else:
        return get_items()


@industry_area_bp.route("/industry-areas/<int:item_id>", methods=['GET', 'PUT', 'DELETE'])
def item_details(item_id):
    # user_id = request.args.get('user_id')  # also can use for capture request GET param
    if request.method == 'GET':
        return get_item_details(item_id)
    elif request.method == 'PUT':
        return update_item(item_id)
    elif request.method == 'DELETE':
        return delete_item(item_id)
    response = {
        'status': 'error',
        'message': 'Bad request body.'
    }
    return jsonify(response), 400


def get_items():
    item_schema = IndustryAreaSchema(many=True)
    item_list = IndustryAreaController.get_items()
    if item_list is None:
        response = {
            'message': 'No area created.'
        }
        return jsonify(response), 404
    result = item_schema.dump(item_list)
    # json_response = json.loads(result)
    response = {
        'data_response': result,
    }
    return jsonify(response), 200


def create_item():
    data = request.get_json()
    if 'industry_name' in data and 'industry_desc' in data:
        error = IndustryAreaController.create_item(data['industry_name'], data['industry_desc'])
        if type(error) is str:
            response = {
                'status': 'error',
                'message': error
            }
            return jsonify(response), 400
        response = {
            'message': "New area registered."
        }
        return jsonify(response), 202
    response = {
        'status': 'error',
        'message': 'Bad request body.'
    }
    return jsonify(response), 400


def get_item_details(item_id):
    item_schema = IndustryAreaSchema()
    item = IndustryAreaController.find_by_id(item_id)
    if item is None:
        response = {
            'message': 'Area does not exist.'
        }
        return jsonify(response), 404
    result = item_schema.dump(item)
    # json_response = json.loads(
    #     result)  # load back as json object so the response won't treat it as db.String and escape it
    response = {
        'data_response': result,
    }
    return jsonify(response), 200


def update_item(item_id):
    data = request.get_json()
    if 'industry_name' in data and 'industry_desc' in data:
        item = IndustryAreaController.find_by_id(item_id)
        # print(user)
        item.industry_name = data['industry_name']
        item.industry_desc = data['industry_desc']

        error = item.commit()
        if type(error) is str:
            response = {
                'message': error
            }
            return jsonify(response), 400
        response = {
            'message': 'Area updated.'
        }
        return jsonify(response), 202
    response = {
        'status': 'error',
        'message': 'Bad request body.'
    }
    return jsonify(response), 400


def delete_item(item_id):
    item = IndustryAreaController.find_by_id(item_id)
    error = item.delete()
    if type(error) is str:
        response = {
            'status': 'error',
            'message': error
        }
        return jsonify(response), 400
    response = {
        'message': 'Area deleted.'
    }
    return jsonify(response), 202
