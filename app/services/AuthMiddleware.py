from flask import Request, Response

from app.config import Config
from app.modules.UserModule.UserController import UserController
from app.services.CASService import CASService
from wsgi import app


class AuthMiddleware:

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # not Flask request - from werkzeug.wrappers import Request
        request = Request(environ)

        if request.method != 'OPTIONS':
            service = request.args.get("service")
            ticket = request.args.get("ticket")
            # print(service, ticket)
            #  make a request to CAS for verification
            root = CASService.get_cas_respond(service, ticket)

            # root = element_tree.getroot()  # to use find, only can apply on ElementTree, if getroot() will return Element
            # print(root)
            if root.find("cas:authenticationSuccess", Config.XML_NAMESPACES) is None:
                response = {
                    'status': 'error',
                    'message': 'Service URL or Service Ticket is invalid'
                }
                import json
                response_object = Response(json.dumps(response), 401)
                # didn't use jsonify() because it return a full flask response object, this dumps() is return a json String
                response_object.headers['content-type'] = "application/json"  # use this to set the content to json
                return response_object(environ, start_response)
            # if service is valid, then continue the network get the username and email first, check the authorise group
            # in AD, cross check with db, if found then continue, else generate new user

            # to find the namespace, root.find("cas:authenticationSuccess/cas:user", Config.NAMESPACES) << use cas:xxx

            username = root.find("cas:authenticationSuccess/cas:user", Config.XML_NAMESPACES).text
            full_name = root.find("cas:authenticationSuccess/cas:attributes/cas:displayName",
                                  Config.XML_NAMESPACES).text
            email = root.find("cas:authenticationSuccess/cas:attributes/cas:userPrincipalName",
                              Config.XML_NAMESPACES).text
            member_of = root.findall("cas:authenticationSuccess/cas:attributes/cas:memberOf",
                                     Config.XML_NAMESPACES)
            # return group of Element, this will use for limit which user to login
            for member_element in member_of:
                # if Config.blackListMemberOf.index(member_element.text):
                if member_element.text in Config.blackListMemberOf:
                    # block the access
                    # print(member_element.text)
                    response = {
                        'status': 'error',
                        'message': 'Account is not authorised to use this service!'
                    }
                    import json
                    response_object = Response(json.dumps(response), 401)
                    response_object.headers['content-type'] = "application/json"
                    return response_object(environ, start_response)

            with app.app_context():
                # print('if acc error, shudnt be here')
                user = UserController.find_user_by_username(username)
                if user is None:
                    error = UserController.create_item(username, full_name, email)
                    if error is not None:
                        response = {
                            'status': 'error',
                            'message': error
                        }
                        import json
                        response_object = Response(json.dumps(response), 400)
                        response_object.headers['content-type'] = "application/json"
                        return response_object(environ, start_response)
                else:
                    environ['QUERY_STRING'] += '&user_id=' + str(user.user_id)
        return self.app(environ, start_response)
