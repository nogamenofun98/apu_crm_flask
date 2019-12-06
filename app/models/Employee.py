from sqlalchemy.sql import expression

from app import db
# from app.models.EmployeeCompany import EmployeeCompany
from app.models.ModelOperation import ModelOperation


class Employee(ModelOperation, db.Model):
    __tablename__ = 'employee'

    employee_id = db.Column(db.Integer, primary_key=True, nullable=False)
    employee_full_name = db.Column(db.String(255), nullable=False)
    employee_image = db.Column(db.BLOB)
    employee_address = db.Column(db.String(255), nullable=False)
    employee_contact_num = db.Column(db.Integer)
    employee_email = db.Column(db.String(255))
    employee_intake_code = db.Column(db.String(255))
    employee_grad_time = db.Column(db.DATE)
    employee_industry_id = db.Column(db.ForeignKey('industry_area.industry_id'), nullable=False, index=True)
    employee_current_company_Id = db.Column(db.ForeignKey('company.company_reg_nun'), nullable=False, index=True)
    employee_last_contact_time = db.Column(db.TIMESTAMP)
    employee_alumnus = db.Column(db.Integer, nullable=False)
    is_hide = db.Column(db.Boolean, nullable=False, server_default=expression.false())

    employee_industry = db.relationship('IndustryArea', backref="employee")

    @staticmethod
    def get_all():
        return Employee.query.all()

# # class below is to jsonify the model
# class EmployeeSchema(ma.ModelSchema):
#     class Meta:
#         model = Employee
