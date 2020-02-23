import base64
import simplejson as json
from io import BytesIO

from flask import Blueprint, jsonify, request
from wordcloud import WordCloud
from app.modules.DashboardModule.DashboardController import DashboardController

home_bp = Blueprint('home_bp', __name__)
graph_fields = ['source', 'conversationEntity', 'conversationType', 'conversationArea', 'conversationPostcode',
                'conversationCity', 'conversationState', 'conversationCountry', 'conversationStatus',
                'conversationDate']


@home_bp.route("/dashboards/word-cloud/<string:source>", methods=['GET'])
def get_word_cloud(source):
    conversations = DashboardController.get_conversations(source)
    texts = " ".join(item for conversation in conversations for item in conversation)
    # same as below
    # for conversation in conversations:
    #     for item in conversation:
    #         print(item)
    #         texts.join(item)
    print(texts)
    wordcloud = WordCloud(width=1280, height=720, max_words=100, background_color="white").generate(texts)
    image = wordcloud.to_image()
    image_object = BytesIO()
    image.save(image_object, "JPEG", quality=100)
    image_object.seek(0)
    base64_string = base64.encodebytes(image_object.getvalue())
    return base64_string
    # return send_file(image_object, mimetype='image/jpeg')


@home_bp.route("/dashboards/report", defaults={'download': None}, methods=['POST'])
@home_bp.route("/dashboards/report/<string:download>", methods=['POST'])
def create_graph(download=None):
    if request.method == 'POST':
        data = request.get_json()
        for field in graph_fields:
            if field not in data:
                response = {
                    'status': 'error',
                    'message': 'Bad request body.'
                }
                return jsonify(response), 400
            else:
                data[field] = str(data[field]).strip()
        # after check fields ok
        session = DashboardController.get_session()
        filter_list = []
        sql_statement = ""
        after_where_statement = ""
        if data["source"] == 'conversation':
            print('conversation')
            if data["conversationType"] == 'count':
                print("count conversation")
                if data["conversationEntity"] == 'company':
                    print("company conversation")
                    sql_statement = "SELECT company.company_name AS name, COUNT(company_email_stat.comp_email_id) AS number FROM company_email_stat INNER JOIN Company ON company_email_stat.comp_comp_id = company.company_reg_num "
                    after_where_statement = " GROUP BY company.company_name ORDER BY COUNT(company_email_stat.comp_email_id) DESC"
                elif data['conversationEntity'] == 'employee-a' or data['conversationEntity'] == 'employee':
                    print("employee conversation")
                    sql_statement = "SELECT employee.employee_full_name AS name, COUNT(alumnus_email_stat.alu_email_id) AS number FROM alumnus_email_stat INNER JOIN Employee ON alumnus_email_stat.alu_alumnus_id = employee.employee_id "
                    after_where_statement = " GROUP BY employee.employee_full_name ORDER BY COUNT(alumnus_email_stat.alu_email_id) DESC"
            elif data["conversationType"] == 'track':
                print("sum open")
                if data["conversationEntity"] == 'company':
                    print("company open")
                    sql_statement = "SELECT company.company_name AS name, SUM(company_email_stat.comp_sum_open) AS number FROM company_email_stat INNER JOIN Company ON company_email_stat.comp_comp_id = company.company_reg_num "
                    after_where_statement = " GROUP BY company.company_name ORDER BY SUM(company_email_stat.comp_sum_open) DESC"

                elif data["conversationEntity"] == 'employee-a' or data['conversationEntity'] == 'employee':
                    print("employee open")
                    sql_statement = "SELECT employee.employee_full_name AS name, SUM(alumnus_email_stat.alu_sum_open) AS number FROM alumnus_email_stat INNER JOIN Employee ON alumnus_email_stat.alu_alumnus_id = employee.employee_id "
                    after_where_statement = " GROUP BY employee.employee_full_name ORDER BY SUM(alumnus_email_stat.alu_sum_open) DESC"

            #  code below is general filter statement for both count and track
            if data["conversationEntity"] == 'company':
                print("company filter")
                if not data['conversationStatus'] == '':
                    filter_list.append("company_email_stat.comp_status_id = :status")
                if not data['conversationDate'] == '':
                    filter_list.append(
                        "MONTH(company_email_stat.comp_open_time) = :month AND YEAR(company_email_stat.comp_open_time) = :year")
                # here run area, postcode, state etc filter
                if not data['conversationArea'] == '':
                    print('area')
                    filter_list.append("company.company_industry_id = :area")
                if not data['conversationPostcode'] == '':
                    print('postcode')
                    filter_list.append("company.company_postcode = :postcode")
                if not data['conversationCity'] == '':
                    print('city')
                    filter_list.append("company.company_city = :city")
                if not data['conversationState'] == '':
                    print('state')
                    filter_list.append("company.company_state = :state")
                if not data['conversationCountry'] == '':
                    print('country')
                    filter_list.append("company.company_country = :country")
            if data['conversationEntity'] == 'employee-a' or data['conversationEntity'] == 'employee':
                print("employee filter")
                if data['conversationEntity'] == 'employee-a':
                    filter_list.append("employee.employee_alumnus = 1")
                elif data['conversationEntity'] == 'employee':  # non alumni
                    filter_list.append("employee.employee_alumnus = 0")

                if not data['conversationStatus'] == '':
                    filter_list.append("alumnus_email_stat.alu_status_id = :status")
                if not data['conversationDate'] == '':
                    filter_list.append(
                        "MONTH(alumnus_email_stat.alu_open_time) = :month AND YEAR(alumnus_email_stat.alu_open_time) = :year")
                # here run area, postcode, state etc filter
                if not data['conversationArea'] == '':
                    print('area')
                    filter_list.append("employee.employee_industry_id = :area")
                if not data['conversationPostcode'] == '':
                    print('postcode')
                    filter_list.append("employee.employee_postcode = :postcode")
                if not data['conversationCity'] == '':
                    print('city')
                    filter_list.append("employee.employee_city = :city")
                if not data['conversationState'] == '':
                    print('state')
                    filter_list.append("employee.employee_state = :state")
                if not data['conversationCountry'] == '':
                    print('country')
                    filter_list.append("employee.employee_country = :country")
            full_where = ""
            first = True
            for item in filter_list:
                if first:
                    full_where += " WHERE "
                    full_where += item
                    first = False
                else:
                    full_where += " AND "
                    full_where += item
                    # full_where += " "
            full_statement = sql_statement + full_where + after_where_statement + " LIMIT 10"
            print(full_statement)
            year, month = None, None
            if not data['conversationDate'] == '':
                year, month = data['conversationDate'].split('-')
            results = None
            if not full_statement == '':
                results = session.execute(full_statement,
                                          {'status': data["conversationStatus"], 'month': month, 'year': year,
                                           'area': data["conversationArea"],
                                           'postcode': data["conversationPostcode"], 'city': data["conversationCity"],
                                           'state': data["conversationState"],
                                           'country': data["conversationCountry"]})
            print(results)
            result_array = []
            if results is not None:
                for result in results:
                    string = json.dumps(dict(result))
                    json_object = json.loads(string)  # load back to json object
                    result_array.append(json_object)
            response = {
                'data_response': result_array,
            }
            return jsonify(response), 200
        elif data["source"] == 'alumni':
            print('alumni')
            if not data['conversationArea'] == '':
                print('area')
                filter_list.append("company.company_industry_id = :area")
            if not data['conversationPostcode'] == '':
                print('postcode')
                filter_list.append("company.company_postcode = :postcode")
            if not data['conversationCity'] == '':
                print('city')
                filter_list.append("company.company_city = :city")
            if not data['conversationState'] == '':
                print('state')
                filter_list.append("company.company_state = :state")
            if not data['conversationCountry'] == '':
                print('country')
                filter_list.append("company.company_country = :country")
            sql_statement = "SELECT company.company_name AS name, COUNT(employee_id) AS number FROM company INNER JOIN employee_company ON company.company_reg_num = employee_company.company_id INNER JOIN employee ON employee_company.alumnus_id = employee.employee_id WHERE employee.employee_alumnus = 1 "
            after_where_statement = " GROUP BY company.company_name ORDER BY COUNT(employee_id) DESC"
            full_where = ""
            first = True
            for item in filter_list:
                full_where += " AND "
                full_where += item
                # full_where += " "
            full_statement = sql_statement + full_where + after_where_statement + " LIMIT 10"
            print(full_statement)
            results = None
            if not full_statement == '':
                results = session.execute(full_statement,
                                          {'area': data["conversationArea"], 'postcode': data["conversationPostcode"],
                                           'city': data["conversationCity"],
                                           'state': data["conversationState"],
                                           'country': data["conversationCountry"]})
            print(results)
            response = {
                'data_response': [dict(row) for row in results],
            }
            return jsonify(response), 200
            # for result in results:
            #     print(result)
            # most alumni
            # no need these: 'conversationEntity', 'conversationType', 'conversationStatus', date

    # return send_file(image_object, mimetype='image/jpeg')
