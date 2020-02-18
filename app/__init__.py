import csv
import os

from flask import json
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, patch_request_class
import flask_excel as excel
from wsgi import app

db = SQLAlchemy()
ma = Marshmallow()
files = UploadSet('files', 'csv')


def create_app():
    from app.config import Config, ConfigDB
    app.config.from_object(Config)
    app.config.from_object(ConfigDB)
    CORS(app)
    db.init_app(app)
    ma.init_app(app)
    configure_uploads(app, files)
    patch_request_class(app)  # set maximum file size, default is 16MB
    excel.init_excel(app)

    with app.app_context():
        from app.models import IndustryArea, EmailStatus, UserRole, User, UserReportDesign, EmployeeCompany, Employee, \
            Company, CompanyEmailStat, AlumnusEmailStat
        db.create_all()  # create tables in database
        if not UserRole.UserRole.get_all():
            #  initialise default super admin role, dev advices to assign the role id to a user first before login into the system
            new = UserRole.UserRole(user_role_description="SuperAdmin",
                                    user_role_json=json.loads(
                                        '{"roles":"full","areas":"full","users":"full","companies":"full","employees":"full","reports":"full","conversations":"full"}'))
            new.save()
        if not IndustryArea.IndustryArea.get_all():
            #  initialise default super admin role, dev advices to assign the role id to a user first before login into the system
            new = IndustryArea.IndustryArea(industry_name="All",
                                            industry_desc="This default area is for user that can manage all company, which separated from admin role.",
                                            is_read_only=True)
            new.save()
        if not EmailStatus.EmailStatus.get_all():
            #  initialise default super admin role, dev advices to assign the role id to a user first before login into the system
            new = EmailStatus.EmailStatus('Lead-Opened', 'New lead')
            new.save()
            new = EmailStatus.EmailStatus('Lead-Processing', 'Discussion undergoing on')
            new.save()
            new = EmailStatus.EmailStatus('Lead-Closed', 'Closed case on the lead')
            new.save()
            new = EmailStatus.EmailStatus('Opportunity-Opened', 'New opportunity')
            new.save()
            new = EmailStatus.EmailStatus('Opportunity-Processing', 'Discussion undergoing on')
            new.save()
            new = EmailStatus.EmailStatus('Opportunity-Closed', 'Closed case on the opportunity')
            new.save()
        migrate = Migrate(app, db,
                          compare_type=True)  # provide Flask Migrate command ability, set column type to detect in migrate
        files_path = Config.UPLOADS_DEFAULT_DEST + 'files/'
        template_path = files_path + "company_template.csv"
        if not os.path.exists(files_path):
            os.makedirs(files_path)
        if not os.path.exists(template_path):
            with open(Config.UPLOADS_DEFAULT_DEST + 'files/company_template.csv', mode='w') as csv_file:
                fieldnames = ['company_reg_num', 'company_name', 'company_size', 'company_industry_id',
                              'company_desc', 'company_address', 'company_postcode', 'company_city', 'company_state',
                              'company_country', 'company_office_contact_num']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

                writer.writeheader()

    from app.modules.LoginModule import routes as login_route
    app.register_blueprint(login_route.login_bp)
    from app.modules.UserModule import routes as user_route
    app.register_blueprint(user_route.user_bp)
    from app.modules.UserRoleModule import routes as role_route
    app.register_blueprint(role_route.user_role_bp)
    from app.modules.IndustryAreaModule import routes as area_route
    app.register_blueprint(area_route.industry_area_bp)
    from app.modules.CompanyModule import routes as comp_route
    app.register_blueprint(comp_route.company_bp)
    from app.modules.EmployeeModule import routes as emp_route
    app.register_blueprint(emp_route.employee_bp)
    from app.modules.EmailStatModule import routes as email_route
    app.register_blueprint(email_route.email_bp)

    from app.services.AuthMiddleware import AuthMiddleware
    app.wsgi_app = AuthMiddleware(app.wsgi_app)
    # must import locally else it will triggered ImportError: cannot import name 'db' from 'app'
