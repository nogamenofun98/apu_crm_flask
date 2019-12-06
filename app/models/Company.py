from sqlalchemy.sql import expression

from app import db
from app.models.ModelOperation import ModelOperation

t_company_contact = db.Table(
    'company_contact',
    db.Column('company_id', db.ForeignKey('company.company_reg_nun'), primary_key=True, nullable=False),
    db.Column('employee_id', db.ForeignKey('employee.employee_id'), primary_key=True, nullable=False, index=True)
)


class Company(ModelOperation, db.Model):
    __tablename__ = 'company'

    company_reg_nun = db.Column(db.Integer, primary_key=True, autoincrement=False)
    company_name = db.Column(db.String(255), nullable=False)
    company_status = db.Column(db.Integer, nullable=False)
    company_size = db.Column(db.Integer, nullable=False)
    company_industry_id = db.Column(db.ForeignKey('industry_area.industry_id'), nullable=False, index=True)
    company_desc = db.Column(db.String(255), nullable=False)
    company_address = db.Column(db.Integer, nullable=False)
    company_office_contact_num = db.Column(db.Integer, nullable=False)
    company_last_contact_time = db.Column(db.TIMESTAMP)
    is_hide = db.Column(db.Boolean, nullable=False, server_default=expression.false())

    company_industry = db.relationship('IndustryArea', backref="company")
    employees = db.relationship('Employee', secondary=t_company_contact, backref="company")

    @staticmethod
    def get_all():
        return Company.query.all()
