from app import db
from app.models.ModelOperation import ModelOperation


class EmployeeCompany(ModelOperation, db.Model):
    __tablename__ = 'employee_company'

    alumnus_id = db.Column(db.ForeignKey('employee.employee_id'), primary_key=True, unique=True)
    company_id = db.Column(db.ForeignKey('company.company_reg_num'), primary_key=True, nullable=False, index=True)
    designation = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(255), nullable=False)
    hired_time = db.Column(db.TIMESTAMP)
    updated_time = db.Column(db.TIMESTAMP)

    company = db.relationship('Company', backref="employee_company")
    employee = db.relationship('Employee', backref="employee_company")

    @staticmethod
    def get_all():
        return EmployeeCompany.query.all()

# class below is to jsonify the model
# class EmpCompSchema(ma.ModelSchema):
#     class Meta:
#         model = EmployeeCompany
