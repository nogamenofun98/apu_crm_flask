import datetime
import re
import flask_excel as excel
from flask import jsonify, request, json, Blueprint

from app import db
from app.models.Schemas import EmployeeSchema, EmpCompSchema
from app.modules.EmployeeModule.EmployeeController import EmployeeController
from app.modules.IndustryAreaModule.IndustryAreaController import IndustryAreaController
from app.modules.UserModule.UserController import UserController
from app.services.CommonServices import CommonServices

employee_bp = Blueprint('employee_bp', __name__)
employee_fields = ['employee_full_name', 'employee_industry_id', 'employee_alumnus', 'employee_address',
                   'employee_postcode', 'employee_city'
    , 'employee_state', 'employee_country', 'employee_contact_num', 'employee_email',
                   'employee_intake_code', 'employee_grad_time']


@employee_bp.route("/employees/export", methods=['GET'])
def export():
    if request.method == 'GET':
        user = UserController.find_by_id(request.args.get("user_id"))
        query_sets = EmployeeController.get_items(user.user_handle_industry)
        column_names = EmployeeController.get_columns_name()
        return excel.make_response_from_query_sets(query_sets, column_names, "xlsx")


@employee_bp.route("/employees/unassigned", methods=['GET'])
def get_unassigned():
    user = UserController.find_by_id(request.args.get("user_id"))
    item_schema = EmployeeSchema(many=True)
    item_list = EmployeeController.get_unassigned_employees(user.user_handle_industry)
    if item_list is None:
        response = {
            'message': 'No employee created.'
        }
        return jsonify(response), 404
    print(item_list)
    result = item_schema.dump(item_list)
    # json_response = json.loads(result)
    response = {
        'data_response': result,
    }
    return jsonify(response), 200


@employee_bp.route("/employees", methods=['GET', 'POST'])
def routes():
    user = UserController.find_by_id(request.args.get("user_id"))
    if request.method == 'POST':
        data = request.get_json()
        if not data['employee_industry_id'] == '':
            is_area_check = CommonServices.check_area(user.user_handle_industry, int(data['employee_industry_id']))
            if not is_area_check:
                response = {
                    'status': 'error',
                    'message': 'Cannot create employee that not belong to logon user\'s industry area'
                }
                return jsonify(response), 400
        return create_item()
    else:
        return get_items(user.user_handle_industry)


@employee_bp.route("/employees/<string:item_id>/jobs", defaults={'company_id': None},
                   methods=['GET', 'POST', 'DELETE'])
@employee_bp.route("/employees/<string:item_id>/jobs/<string:company_id>", methods=['GET', 'POST', 'DELETE'])
def get_jobs(item_id, company_id=None):
    user = UserController.find_by_id(request.args.get("user_id"))
    item_schema = EmpCompSchema(many=True)
    item = EmployeeController.find_by_id(item_id)
    is_area_check = True
    if item is not None:
        if item.employee_industry_id is not None:
            is_area_check = CommonServices.check_area(user.user_handle_industry, int(item.employee_industry_id))
        if is_area_check:
            if request.method == 'GET':
                jobs = EmployeeController.get_jobs(item_id)
                result = item_schema.dump(jobs)
                # json_response = json.loads(result)
                response = {
                    'data_response': result,
                }
                return jsonify(response), 200
            elif request.method == 'DELETE':
                item = EmployeeController.find_job(item_id, company_id)
                db.session.delete(item)
                error = item.commit()
                if type(error) is str:
                    response = {
                        'message': error
                    }
                    return jsonify(response), 400
                response = {
                    'message': 'Job deleted.'
                }
                return jsonify(response), 202
            elif request.method == 'POST':
                data = request.get_json()
                if not str(data['employee_company_Id']) == '':
                    job_error = EmployeeController.add_working_job(item_id,
                                                                   data['employee_company_Id'],
                                                                   data['job_designation'],
                                                                   data['job_department'],
                                                                   data['job_hired_date'], data['is_current_job'])
                    if type(job_error) is str:
                        response = {
                            'status': 'error',
                            'message': job_error
                        }
                        return jsonify(response), 400
                    response = {
                        'message': 'Job Added.'
                    }
                    return jsonify(response), 200
        else:
            response = {
                'status': 'error',
                'message': 'Cannot perform action on employee that not belong to logon user\'s industry area'
            }
            return jsonify(response), 400
    response = {
        'status': 'error',
        'message': 'Employee not found!'
    }
    return jsonify(response), 400


@employee_bp.route("/employees/check-emp/<string:email>", methods=['GET'])
def check_reg_num(email):
    item_schema = EmployeeSchema()
    item = EmployeeController.find_by_contact(email)
    if item is None:
        response = {
            'message': 'Employee does not exist.'
        }
        return jsonify(response), 200  # avoid error message on frontend, so 200
    result = item_schema.dump(item)
    # json_response = json.loads(
    #     result)  # load back as json object so the response won't treat it as db.String and escape it
    response = {
        'data_response': result,
    }
    return jsonify(response), 200


@employee_bp.route("/employees/<string:item_id>", methods=['GET', 'PUT', 'DELETE'])
def item_details(item_id):
    user = UserController.find_by_id(request.args.get("user_id"))
    item = EmployeeController.find_by_id(item_id)
    is_area_check = True
    if item is not None:
        if item.employee_industry_id is not None:
            is_area_check = CommonServices.check_area(user.user_handle_industry, int(item.employee_industry_id))
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
                'message': 'Cannot perform action on employee that not belong to logon user\'s industry area'
            }
            return jsonify(response), 400
    response = {
        'status': 'error',
        'message': 'Employee not found!'
    }
    return jsonify(response), 400


def get_items(industry_area):
    item_schema = EmployeeSchema(many=True)
    item_list = EmployeeController.get_items(industry_area)
    if item_list is None:
        response = {
            'message': 'No employee created.'
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
    for field in employee_fields:
        if field not in data:
            response = {
                'status': 'error',
                'message': 'Bad request body.'
            }
            return jsonify(response), 400

    error = EmployeeController.create_item(employee_full_name=data['employee_full_name'],
                                           employee_industry_id=data['employee_industry_id'],
                                           employee_alumnus=data['employee_alumnus'],
                                           employee_address=data['employee_address'],
                                           employee_postcode=data['employee_postcode'],
                                           employee_city=data['employee_city']
                                           , employee_state=data['employee_state'],
                                           employee_country=data['employee_country'],
                                           employee_contact_num=data['employee_contact_num'],
                                           employee_email=data['employee_email'],
                                           employee_intake_code=data['employee_intake_code'],
                                           employee_grad_time=data['employee_grad_time'])
    if type(error) is str:
        response = {
            'status': 'error',
            'message': error
        }
        return jsonify(response), 400
    #  if employee_current_company_Id is not null, then insert into employeecompany table
    # if not str(data['employee_current_company_Id']) == '':
    #     job_error = EmployeeController.add_working_job(error.employee_id, data['employee_current_company_Id'],
    #                                                    data['current_job_designation'], data['current_job_department'],
    #                                                    data['current_job_hired_date'], True)
    #     if type(job_error) is str:
    #         response = {
    #             'status': 'error',
    #             'message': error + ", but the employee info still created successfully."
    #         }
    #         return jsonify(response), 400
    response = {
        'message': "New employee registered."
    }
    return jsonify(response), 202


def get_item_details(item_id, isCheck=False):
    item_schema = EmployeeSchema()
    item = EmployeeController.find_by_id(item_id)
    if item is None:
        response = {
            'message': 'Employee does not exist.'
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
    for field in employee_fields:
        if field not in data:
            response = {
                'status': 'error',
                'message': 'Bad request body.'
            }
            return jsonify(response), 400
    item = EmployeeController.find_by_id(item_id)
    is_error = False
    error_message = ""
    if data['employee_full_name'].strip() == '':
        is_error = True
        error_message += "Must provide full name"
    if not type(data['employee_alumnus']) == bool:
        is_error = True
        if error_message is not "":
            error_message += ", "
        error_message += "Must set is APU alumnus or not"

    if not data['employee_contact_num'] == '':
        if not re.match('^(\\+?6?0)[0-9]{1,2}-*[0-9]{7,8}$', str(data['employee_contact_num'])):
            is_error = True
            if error_message is not "":
                error_message += ", "
            error_message += "Contact number must be in correct format! Received value: " + str(
                data['employee_contact_num'])

    if not data['employee_postcode'] == '':
        if not re.match('^[0-9]{1,6}$', str(data['employee_postcode'])):
            is_error = True
            if error_message is not "":
                error_message += ", "
            error_message += "Postcode must be in correct format! Received value: " + str(data['employee_postcode'])
    if not str(data['employee_grad_time']) == "":
        try:
            datetime.datetime.strptime(data['employee_grad_time'], '%Y-%m-%d')
        except ValueError as ex:
            is_error = True
            if error_message is not "":
                error_message += ", "
            error_message += "Graduation Date format error: " + str(data['employee_grad_time'])

    if not is_error:
        if not data['employee_full_name'].strip() == "":
            item.employee_address = data['employee_full_name']
        if not data['employee_alumnus'] == "":
            item.employee_alumnus = data['employee_alumnus']
        if not data['employee_address'].strip() == "":
            item.employee_address = data['employee_address']
        if not data['employee_industry_id'] == "":
            item.employee_industry_id = data['employee_industry_id']
        if not data['employee_postcode'].strip() == "":
            item.employee_postcode = data['employee_postcode']
        if not data['employee_city'].strip() == "":
            item.employee_city = data['employee_city']
        if not data['employee_state'].strip() == "":
            item.employee_state = data['employee_state']
        if not data['employee_country'].strip() == "":
            item.employee_country = data['employee_country']
        if not data['employee_contact_num'].strip() == "":
            item.employee_contact_num = data['employee_contact_num']
        if not data['employee_grad_time'].strip() == "":
            item.employee_grad_time = data['employee_grad_time']
        if not data['employee_email'].strip() == "":
            item.employee_email = data['employee_email']
        if not data['employee_intake_code'].strip() == "":
            item.employee_intake_code = data['employee_intake_code']
        # if not data['employee_current_company_Id'].strip() == "":
        #     item.employee_current_company_Id = data['employee_current_company_Id']
        error = item.commit()
        if type(error) is str:
            response = {
                'message': error
            }
            return jsonify(response), 400
        response = {
            'message': 'Employee updated.'
        }
        return jsonify(response), 202
    else:
        response = {
            'status': 'error',
            'message': error_message
        }
        return jsonify(response), 400


def delete_item(item_id):
    item = EmployeeController.find_by_id(item_id)
    item.is_hide = True
    error = item.commit()
    if type(error) is str:
        response = {
            'message': error
        }
        return jsonify(response), 400
    response = {
        'message': 'Employee soft deleted.'
    }
    return jsonify(response), 202
