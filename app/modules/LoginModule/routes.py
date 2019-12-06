from flask import Blueprint

from app.config import Config
from app.models.Schemas import UserSchema
from app.modules.UserModule.UserController import UserController
from app.services.CASService import CASService

login_bp = Blueprint('login_bp', __name__)


#  auth with url and ticket, if ok then return back the user info to the ionic app
@login_bp.route("/auth/", methods=['GET'])
def login():
    # service = request.args.get("service")
    # ticket = request.args.get("ticket")
    # print(service, ticket)
    # root = CASService.get_cas_respond(service, ticket)
    root = CASService.get_root()
    # print(root)
    username = root.find("cas:authenticationSuccess/cas:user", Config.XML_NAMESPACES).text
    user_schema = UserSchema()
    user = user_schema.dump(UserController.find_user_by_username(username))
    #  print(user)
    response = {
        'data_response': user,
        'status_code': 202
    }
    from flask import jsonify
    return jsonify(response), 202
