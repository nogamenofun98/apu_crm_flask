import re

from flask import jsonify, request, json, Blueprint
from flask_uploads import UploadNotAllowed

from app import db, files
from app.models.Schemas import CompanySchema
from app.modules.CompanyModule.CompanyController import CompanyController
from app.modules.UserModule.UserController import UserController
from app.services.CommonServices import CommonServices

company_bp = Blueprint('company_bp', __name__)
company_fields = ['company_reg_num', 'company_name', 'company_size', 'company_industry_id',
                  'company_desc', 'company_office_contact_num', 'company_address', 'company_postcode', 'company_city',
                  'company_state', 'company_country']


@company_bp.route("/companies/uploader", methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        # check if the post request has the file part
        # if 'csv' not in request.files:
        # file = request.files['csv']
        # print(file)
        try:
            filename = files.save(request.files['csv'])
        except UploadNotAllowed as err:
            response = {
                'status': 'test',
                'message': "File upload is not allowed!" + str(err)
            }
            return jsonify(response), 400
        # below is the for loop code and creation code
        user = UserController.find_by_id(request.args.get("user_id"))
        from app.config import Config
        with open(Config.UPLOADS_DEFAULT_DEST + "files/" + filename, mode='r') as csv_file:
            import csv
            csv_reader = csv.DictReader(csv_file)
            error_message = ""
            for row in csv_reader:
                is_area_check = CommonServices.check_area(user.user_handle_industry, int(row['company_industry_id']))
                if not is_area_check:
                    error_message += "\r\n" + row[
                        'company_reg_num'] + ": Cannot create company that not belong to logon user\'s industry area. "
                else:
                    error = CompanyController.create_item(company_reg_num=row['company_reg_num'],
                                                          company_name=row['company_name'],
                                                          company_size=row['company_size'],
                                                          company_industry_id=row['company_industry_id'],
                                                          company_desc=row['company_desc'],
                                                          company_office_contact_num=row[
                                                              'company_office_contact_num'],
                                                          company_address=row['company_address']
                                                          , company_postcode=row['company_postcode'],
                                                          company_city=row['company_city'],
                                                          company_state=row['company_state'],
                                                          company_country=row['company_country'])
                    if type(error) is str:
                        error_message += "\r\n" + row['company_reg_num'] + ": " + error
        response = {
            'status': 'done',
            'message': "All imported" if error_message == "" else error_message
        }
        return jsonify(response), 200 if error_message == "" else 400
    else:
        response = {
            'status': 'success',
            'url': files.url('company_template.csv')
        }
        return jsonify(response), 200


@company_bp.route("/companies", methods=['GET', 'POST'])
def routes():
    user = UserController.find_by_id(request.args.get("user_id"))
    if request.method == 'POST':
        data = request.get_json()
        if data['company_industry_id'] == '':
            response = {
                'status': 'error',
                'message': 'Cannot leave industry area empty'
            }
            return jsonify(response), 400
        is_area_check = CommonServices.check_area(user.user_handle_industry, int(data['company_industry_id']))
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
        is_area_check = CommonServices.check_area(user.user_handle_industry, int(item.company_industry_id))
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
    if type(error) is str:
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
    is_error = False
    error_message = ""
    item = CompanyController.find_by_id(item_id)
    if item is not None:
        is_error = True
        error_message += "Registration number duplicated! Received value: " + str(
            item_id)

    if not re.match('^(\\+?6?0)[0-9]{1,2}-*[0-9]{7,8}$', str(data['company_office_contact_num'])):
        is_error = True
        error_message += "Contact number must be in correct format! Received value: " + str(
            data['company_office_contact_num'])

    if not data['company_address'] == '':
        if not re.match('^[0-9]{1,6}$', str(data['company_postcode'])):
            is_error = True
            if error_message is not "":
                error_message += ", "
            error_message += "Postcode must be in correct format! Received value: " + str(data['company_postcode'])
    if not is_error:
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
    else:
        response = {
            'status': 'error',
            'message': error_message
        }
        return jsonify(response), 400


def delete_item(item_id):
    item = CompanyController.find_by_id(item_id)
    item.is_hide = True
    db.session.commit()
    # error = item.delete()
    # if type(error) is str:
    #     response = {
    #         'status': 'error',
    #         'message': error
    #     }
    #     return jsonify(response), 400
    response = {
        'message': 'Company soft deleted.'
    }
    return jsonify(response), 202
