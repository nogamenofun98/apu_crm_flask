from app import db
from app.models.ModelOperation import ModelOperation


class EmployeeCompany(ModelOperation, db.Model):
    __tablename__ = 'employee_company'

    alumnus_id = db.Column(db.ForeignKey('employee.employee_id'), primary_key=True, index=True)
    company_id = db.Column(db.ForeignKey('company.company_reg_num'), primary_key=True, index=True)
    designation = db.Column(db.String(255))
    department = db.Column(db.String(255))
    hired_time = db.Column(db.TIMESTAMP)
    updated_time = db.Column(db.TIMESTAMP)
    is_current_job = db.Column(db.Boolean, nullable=False)

    company = db.relationship('Company', backref="employee_company")
    employee = db.relationship('Employee', backref="employee_company")

    def __init__(self, alumnus_id, company_id):
        super().__init__()
        self.alumnus_id = alumnus_id
        self.company_id = company_id

    @staticmethod
    def get_all():
        return EmployeeCompany.query.all()

# class below is to jsonify the model
# class EmpCompSchema(ma.ModelSchema):
#     class Meta:
#         model = EmployeeCompany
