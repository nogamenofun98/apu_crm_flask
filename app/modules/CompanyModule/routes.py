from flask import jsonify, request, json, Blueprint

from app import db
from app.models.Schemas import CompanySchema
from app.modules.CompanyModule.CompanyController import CompanyController
from app.modules.UserModule.UserController import UserController

company_bp = Blueprint('company_bp', __name__)
company_fields = ['company_reg_num', 'company_name', 'company_size', 'company_industry_id',
                  'company_desc', 'company_office_contact_num', 'company_address', 'company_postcode', 'company_city',
                  'company_state', 'company_country']


@company_bp.route("/companies", methods=['GET', 'POST'])
def routes():
    user = UserController.find_by_id(request.args.get("user_id"))
    if request.method == 'POST':
        data = request.get_json()
        is_area_check = check_area(user.user_handle_industry, int(data['company_industry_id']))
        if not is_area_check:
            response = {
                'status': 'error',
                'message': 'Cannot create company that not belong to logon user\'s industry area'
            }
            return jsonify(response), 400
        return create_item()
    else:
        return get_items(user.user_handle_industry)


@company_bp.route("/companies/check-comp-reg-num/<string:item_id>", methods=['GET'])
def check_reg_num(item_id):
    return get_item_details(item_id, True)


@company_bp.route("/companies/<string:item_id>", methods=['GET', 'PUT', 'DELETE'])
def item_details(item_id):
    user = UserController.find_by_id(request.args.get("user_id"))
    item = CompanyController.find_by_id(item_id)
    if item is not None:
        is_area_check = check_area(user.user_handle_industry, int(item.company_industry_id))
        if is_area_check:
            if request.method == 'GET':
                return get_item_details(item_id)
            elif request.method == 'PUT':
                return update_item(item_id)
            elif request.method == 'DELETE':
                return delete_item(item_id)
        else:
            response = {
                'status': 'error',
                'message': 'Cannot perform action on company that not belong to logon user\'s industry area'
            }
            return jsonify(response), 400
    response = {
        'status': 'error',
        'message': 'Company not found!'
    }
    return jsonify(response), 400


# return true when is belong to "All, read-only", return true also when is same id, return false when is diff id
def check_area(user_industry, data_industry_id=None):
    # print("user area id: ", user_industry.industry_id, ", data area id: ", data_industry_id)
    if user_industry.is_read_only and user_industry.industry_name == "All":
        return True
    else:
        if data_industry_id is not None:
            if user_industry.industry_id == data_industry_id:
                return True
        return False


def get_items(industry_area):
    item_schema = CompanySchema(many=True)
    item_list = CompanyController.get_items(industry_area)
    if item_list is None:
        response = {
            'message': 'No company created.'
        }
        return jsonify(response), 404
    result = item_schema.dumps(item_list)
    json_response = json.loads(result)
    response = {
        'data_response': json_response,
    }
    return jsonify(response), 200


def create_item():
    data = request.get_json()
    # print(data)
    for field in company_fields:
        if field not in data:
            response = {
                'status': 'error',
                'message': 'Bad request body.'
            }
            return jsonify(response), 400
    error = CompanyController.create_item(company_reg_num=data['company_reg_num'], company_name=data['company_name'],
                                          company_size=data['company_size'],
                                          company_industry_id=data['company_industry_id'],
                                          company_desc=data['company_desc'],
                                          company_office_contact_num=data['company_office_contact_num'],
                                          company_address=data['company_address']
                                          , company_postcode=data['company_postcode'],
                                          company_city=data['company_city'], company_state=data['company_state'],
                                          company_country=data['company_country'])
    if error is not None:
        response = {
            'status': 'error',
            'message': error
        }
        return jsonify(response), 400
    response = {
        'message': "New company registered."
    }
    return jsonify(response), 202


def get_item_details(item_id, isCheck=False):
    item_schema = CompanySchema()
    item = CompanyController.find_by_id(item_id)
    if item is None:
        response = {
            'message': 'Company does not exist.'
        }
        if isCheck:
            return jsonify(response), 200
        else:
            return jsonify(response), 404
    result = item_schema.dumps(item)
    json_response = json.loads(
        result)  # load back as json object so the response won't treat it as db.String and escape it
    response = {
        'data_response': json_response,
    }
    return jsonify(response), 200


def update_item(item_id):
    data = request.get_json()
    for field in company_fields:
        if field not in data:
            response = {
                'status': 'error',
                'message': 'Bad request body.'
            }
            return jsonify(response), 400
    item = CompanyController.find_by_id(item_id)
    item.company_reg_num = data['company_reg_num']
    item.company_name = data['company_name']
    item.company_size = data['company_size']
    item.company_industry_id = data['company_industry_id']
    item.company_desc = data['company_desc']
    item.company_office_contact_num = data['company_office_contact_num']
    item.company_address = data['company_address']
    item.company_postcode = data['company_postcode']
    item.company_city = data['company_city']
    item.company_state = data['company_state']
    item.company_country = data['company_country']

    db.session.commit()
    response = {
        'message': 'Company updated.'
    }
    return jsonify(response), 202


def delete_item(item_id):
    item = CompanyController.find_by_id(item_id)
    error = item.delete()
    if error is not None:
        response = {
            'status': 'error',
            'message': error
        }
        return jsonify(response), 400
    response = {
        'message': 'Company deleted.'
    }
    return jsonify(response), 202
