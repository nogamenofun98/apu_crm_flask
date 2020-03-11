from flask import Blueprint, request, jsonify, json
from sqlalchemy.exc import SQLAlchemyError
import flask_excel as excel
from app import db
from app.models.EmailStatus import EmailStatus
from app.models.Schemas import EmailStatusSchema
from app.modules.CompanyModule.CompanyController import CompanyController
from app.modules.EmailStatModule.EmailStatController import EmailStatController
from app.modules.EmployeeModule.EmployeeController import EmployeeController
from app.modules.UserModule.UserController import UserController
from app.services.CommonServices import CommonServices

email_bp = Blueprint('email_bp', __name__)


@email_bp.route("/conversations/status", methods=['GET'])
def get_status():
    status_list = EmailStatus.get_all()
    item_schema = EmailStatusSchema(many=True)
    result = item_schema.dump(status_list)
    response = {
        'data_response': result,
    }
    return jsonify(response), 200


@email_bp.route("/conversations/<string:source>", methods=['GET', 'POST'])
def routes(source):
    user = UserController.find_by_id(request.args.get("user_id"))
    if request.method == 'POST':
        data = request.get_json()
        if data["target_id"] == "":
            response = {
                'status': 'error',
                'message': 'Target user is empty'
            }
            return jsonify(response), 400
        if source == "employee":
            employee = EmployeeController.find_by_id(data["target_id"])
            if employee is None:
                response = {
                    'status': 'error',
                    'message': 'Target id not found'
                }
                return jsonify(response), 400
            industry_id = employee.employee_industry_id
        else:
            company = CompanyController.find_by_id(data["target_id"])
            if company is None:
                response = {
                    'status': 'error',
                    'message': 'Target id not found'
                }
                return jsonify(response), 400
            industry_id = company.company_industry_id
        is_area_check = CommonServices.check_area(user.user_handle_industry, int(industry_id))
        if not is_area_check:
            response = {
                'status': 'error',
                'message': 'Cannot create conversation that not belong to logon user\'s industry area'
            }
            return jsonify(response), 400
        return create_item(source, user.user_id)
    else:
        return get_items(source, user.user_handle_industry)


@email_bp.route("/conversations/<string:source>/export", methods=['GET'])
def export(source):
    if request.method == 'GET':
        user = UserController.find_by_id(request.args.get("user_id"))
        item_list = EmailStatController.get_items(source, user.user_handle_industry)

        result_list = []
        for item in item_list:
            result = serialize_field(source, item)
            result_list.append(result)
        print(result_list)
        # column_list = ["email_id", "user_id", "user_full_name", "target_id", "target_name", "open_time", "sum_open",
        #                "status_id", "status_name", "industry_area_id", "industry_area_name", "conversation", "updated_time"]
        return excel.make_response_from_records(result_list, "xlsx")


# public route, no need token authentication, is put in email, suppress any error
@email_bp.route("/track/conversations/<string:source>/<string:item_id>", methods=['GET'])
def track(source, item_id):
    print("tracking")
    url = request.args.get('url')
    print(url)
    #  insert track record
    import datetime
    item = EmailStatController.find_by_id(source, item_id)
    if item is not None:
        if source == "employee":
            # item.alu_open_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            item.alu_sum_open = item.alu_sum_open + 1
            item.commit()
        else:
            # item.comp_open_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            item.comp_sum_open = item.comp_sum_open + 1
            item.commit()
    from flask import redirect
    return redirect(url)


@email_bp.route("/conversations/<string:source>/<string:item_id>", methods=['GET', 'PUT'])
def item_details(source, item_id):
    user = UserController.find_by_id(request.args.get("user_id"))
    item = EmailStatController.find_by_id(source, item_id)
    if item is not None:
        if source == "employee":
            employee = EmployeeController.find_by_id(item.alu_alumnus_id)
            if employee is None:
                response = {
                    'status': 'error',
                    'message': 'Target id not found'
                }
                return jsonify(response), 400
            industry_id = employee.employee_industry_id
        else:
            company = CompanyController.find_by_id(item.comp_comp_id)
            if company is None:
                response = {
                    'status': 'error',
                    'message': 'Target id not found'
                }
                return jsonify(response), 400
            industry_id = company.company_industry_id
        is_area_check = CommonServices.check_area(user.user_handle_industry, int(industry_id))
        if is_area_check:
            if request.method == 'GET':
                return get_item_details(source, item_id)
            elif request.method == 'PUT':
                return update_item(source, item_id)
        else:
            response = {
                'status': 'error',
                'message': 'Cannot perform action on conversation that not belong to logon user\'s industry area'
            }
            return jsonify(response), 400
    response = {
        'status': 'error',
        'message': 'Conversation not found!'
    }
    return jsonify(response), 400


def get_items(source, user_handle_industry):
    item_list = EmailStatController.get_items(source, user_handle_industry)
    if item_list is None:
        response = {
            'message': 'No conversation created.'
        }
        return jsonify(response), 404
    result_list = []
    for item in item_list:
        result = serialize_field(source, item)
        result_list.append(result)
    result_list = sorted(result_list, key=lambda i: i['email_id'], reverse=True)
    response = {
        'data_response': result_list,
    }
    return jsonify(response), 200


def get_item_details(source, item_id):
    item = EmailStatController.find_by_id(source, item_id)
    if item is None:
        response = {
            'message': 'Conversation does not exist.'
        }
        return jsonify(response), 404

    result = serialize_field(source, item)
    # get user name, get target name, get target industry area, status name

    response = {
        'data_response': result,
    }
    return jsonify(response), 200


def create_item(source, user_id):
    data = request.get_json()
    if 'target_id' in data and 'conversation' in data and "status_id" in data:
        error = EmailStatController.create_item(source, user_id, data["target_id"], data["conversation"],
                                                data["status_id"])
        if type(error) is str:
            response = {
                'status': 'error',
                'message': error
            }
            return jsonify(response), 400
        response = {
            'message': "New conversation created."
        }
        return jsonify(response), 202
    response = {
        'status': 'error',
        'message': 'Bad request body.'
    }
    return jsonify(response), 400


def update_item(source, item_id):
    user = UserController.find_by_id(request.args.get("user_id"))
    # import datetime
    # updated_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = request.get_json()
    if 'target_id' in data and 'conversation' in data and "status_id" in data:
        return create_item(source, user.user_id) # changed from edit conversation to create new conversation every time user update it
        # email = EmailStatController.find_by_id(source, item_id)
        # if source == "employee":
        #     email.alu_user_id = user.user_id  # to show latest user who edit the record
        #     email.alu_alumnus_id = data['target_id']
        #     email.alu_conversation = data['conversation']
        #     email.alu_status_id = data['status_id']
        #     email.alu_updated_time = updated_time
        # else:
        #     email.comp_user_id = user.user_id  # to show latest user who edit the record
        #     email.comp_comp_id = data['target_id']
        #     email.comp_conversation = data['conversation']
        #     email.comp_status_id = data['status_id']
        #     email.comp_updated_time = updated_time
        #
        # error = email.commit()
        # if type(error) is str:
        #     response = {
        #         'message': error
        #     }
        #     return jsonify(response), 400
        # response = {
        #     'message': 'Conversation updated.'
        # }
        # return jsonify(response), 202
    response = {
        'status': 'error',
        'message': 'Bad request body.'
    }
    return jsonify(response), 400


def serialize_field(source, item):
    result = {}
    if source == "employee":
        user = UserController.find_by_id(item.alu_user_id)
        employee = EmployeeController.find_by_id(item.alu_alumnus_id)
        status = EmailStatus.query.filter_by(status_id=item.alu_status_id).first()
        result["email_id"] = item.alu_email_id
        result["user_full_name"] = user.user_full_name
        result["user_id"] = item.alu_user_id
        result["target_name"] = employee.employee_full_name
        result["target_id"] = item.alu_alumnus_id
        result["open_time"] = item.alu_open_time
        result["sum_open"] = item.alu_sum_open
        result["status_name"] = status.status_name
        result["status_id"] = item.alu_status_id
        result["industry_area_name"] = employee.employee_industry.industry_name
        result["industry_area_id"] = employee.employee_industry_id
        result["conversation"] = item.alu_conversation
        result["updated_time"] = item.alu_updated_time

    else:
        user = UserController.find_by_id(item.comp_user_id)
        company = CompanyController.find_by_id(item.comp_comp_id)
        status = EmailStatus.query.filter_by(status_id=item.comp_status_id).first()
        result["email_id"] = item.comp_email_id
        result["user_full_name"] = user.user_full_name
        result["user_id"] = item.comp_user_id
        result["target_name"] = company.company_name
        result["target_id"] = item.comp_comp_id
        result["open_time"] = item.comp_open_time
        result["sum_open"] = item.comp_sum_open
        result["status_name"] = status.status_name
        result["status_id"] = item.comp_status_id
        result["industry_area_name"] = company.company_industry.industry_name
        result["industry_area_id"] = company.company_industry_id
        result["conversation"] = item.comp_conversation
        result["updated_time"] = item.comp_updated_time
    return result
