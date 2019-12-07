from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from wsgi import app

db = SQLAlchemy()
ma = Marshmallow()


def create_app():
    from app.config import Config, ConfigDB
    app.config.from_object(Config)
    app.config.from_object(ConfigDB)
    CORS(app)
    db.init_app(app)
    ma.init_app(app)
    with app.app_context():
        from app.models import IndustryArea, EmailStatus, UserRole, User, UserReportDesign, EmployeeCompany, Employee, \
            Company, CompanyEmailStat, AlumnusEmailStat
        db.create_all()
    migrate = Migrate(app, db)  # provide Flask Migrate command ability

    from app.modules.LoginModule import routes as login_route
    app.register_blueprint(login_route.login_bp)
    from app.modules.UserModule import routes as user_route
    app.register_blueprint(user_route.user_bp)
    from app.modules.UserRoleModule import routes as role_route
    app.register_blueprint(role_route.user_role_bp)
    from app.modules.IndustryAreaModule import routes as area_route
    app.register_blueprint(area_route.industry_area_bp)

    from app.services.AuthMiddleware import AuthMiddleware
    app.wsgi_app = AuthMiddleware(app.wsgi_app)
    # must import locally else it will triggered ImportError: cannot import name 'db' from 'app'
