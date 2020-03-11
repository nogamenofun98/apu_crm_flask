import re
import flask_excel as excel
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


@company_bp.route("/companies/<string:item_id>/contacts", defaults={'employee_id': None},
                  methods=['POST', 'DELETE'])
@company_bp.route("/companies/<string:item_id>/contacts/<string:employee_id>", methods=['POST', 'DELETE'])
def get_contacts(item_id, employee_id=None):
    print("adding contact")
    item = CompanyController.find_by_id(item_id)
    from app.modules.EmployeeModule.EmployeeController import EmployeeController
    employee = EmployeeController.find_by_id(employee_id)
    if item is not None:
        if employee is not None:
            if request.method == 'DELETE':
                result = CompanyController.contact_action(item, employee, 'delete')
                response = {
                    'message': result
                }
                return jsonify(response), 202
            elif request.method == 'POST':
                result = CompanyController.contact_action(item, employee, 'add')
                response = {
                    'message': result
                }
                return jsonify(response), 200
        else:
            response = {
                'status': 'error',
                'message': 'Employee not found!'
            }
            return jsonify(response), 400
    response = {
        'status': 'error',
        'message': 'Company not found!'
    }
    return jsonify(response), 400


@company_bp.route("/companies/<string:item_id>/employee-list", methods=['GET'])
def get_employee_list(item_id):
    results = CompanyController.get_employees(item_id)
    result_list = []
    for item in results:
        result = serialize_field(item)
        result_list.append(result)
    response = {
        'data_response': result_list,
    }
    return jsonify(response), 200


@company_bp.route("/companies/<string:item_id>/employee-list/download", methods=['GET'])
def download_employee_list(item_id):
    results = CompanyController.get_employees(item_id)
    result_list = []
    for item in results:
        result = serialize_field(item)
        result_list.append(result)
    return excel.make_response_from_records(result_list, "xlsx")


def serialize_field(item):
    result = {}
    print(item)
    result["employee_id"] = item[2].employee_id
    result["full_name"] = item[2].employee_full_name
    result["employee_email"] = item[2].employee_email
    result["employee_contact_num"] = item[2].employee_contact_num
    result["employee_address"] = item[2].employee_address
    result["employee_postcode"] = item[2].employee_postcode
    result["employee_city"] = item[2].employee_city
    result["employee_state"] = item[2].employee_state
    result["employee_country"] = item[2].employee_country
    result["is_Alumni"] = item[2].employee_alumnus
    result["employee_grad_time"] = item[2].employee_grad_time
    result["intake_code"] = item[2].employee_intake_code
    result["is_hide"] = item[2].is_hide
    result["designation"] = item[1].designation
    result["department"] = item[1].department
    result["hired_time"] = item[1].hired_time

    return result


@company_bp.route("/companies/export", methods=['GET'])
def export():
    if request.method == 'GET':
        user = UserController.find_by_id(request.args.get("user_id"))
        query_sets = CompanyController.get_items(user.user_handle_industry)
        column_names = CompanyController.get_columns_name()
        return excel.make_response_from_query_sets(query_sets, column_names, "xlsx")


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
    result = item_schema.dump(item_list)
    # json_response = json.loads(result)
    response = {
        'data_response': result,
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
    result = item_schema.dump(item)
    # json_response = json.loads(
    #     result)  # load back as json object so the response won't treat it as db.String and escape it
    response = {
        'data_response': result,
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
    company_reg_num = str(data['company_reg_num']).strip()
    company_name = str(data['company_name']).strip()
    company_size = str(data['company_size']).strip()
    company_desc = str(data['company_desc']).strip()

    if company_reg_num == '':
        is_error = True
        if error_message is not "":
            error_message += ", "
        error_message += "Registration number cannot be empty!"
    else:
        if item.company_reg_num != data['company_reg_num']:
            new_item = CompanyController.find_by_id(data['company_reg_num'])
            if new_item is not None:
                is_error = True
                error_message += "Registration number duplicated! Received value: " + str(
                    item_id)

    if company_name == '':
        is_error = True
        if error_message is not "":
            error_message += ", "
        error_message += "Name cannot be empty!"
    if company_size == '':
        is_error = True
        if error_message is not "":
            error_message += ", "
        error_message += "Size cannot be empty!"
    if company_desc == '':
        is_error = True
        if error_message is not "":
            error_message += ", "
        error_message += "Description cannot be empty!"

    if not re.match('^(\\+?6?0)[0-9]{1,2}-*[0-9]{7,8}$', str(data['company_office_contact_num'])):
        is_error = True
        if error_message is not "":
            error_message += ", "
        error_message += "Contact number must be in correct format! Received value: " + str(
            data['company_office_contact_num'])

    if not data['company_postcode'] == '':
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

        error = item.commit()
        if type(error) is str:
            response = {
                'message': error
            }
            return jsonify(response), 400
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
    item.company_reg_num = item.company_reg_num + "_hide"
    error = item.commit()
    if type(error) is str:
        response = {
            'message': error
        }
        return jsonify(response), 400
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
