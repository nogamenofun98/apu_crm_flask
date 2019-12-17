from sqlalchemy.sql import expression

from app import db
from app.models.ModelOperation import ModelOperation

t_company_contact = db.Table(
    'company_contact',
    db.Column('company_id', db.ForeignKey('company.company_reg_num'), primary_key=True, nullable=False),
    db.Column('employee_id', db.ForeignKey('employee.employee_id'), primary_key=True, nullable=False, index=True)
)


class Company(ModelOperation, db.Model):
    __tablename__ = 'company'

    company_reg_num = db.Column(db.String(255), primary_key=True, autoincrement=False)
    company_name = db.Column(db.String(255), nullable=False)
    company_size = db.Column(db.Integer, nullable=False)
    company_industry_id = db.Column(db.ForeignKey('industry_area.industry_id'), nullable=False, index=True)
    company_desc = db.Column(db.String(255), nullable=False)
    company_address = db.Column(db.String(255))
    company_postcode = db.Column(db.Integer)
    company_city = db.Column(db.String(255))
    company_state = db.Column(db.String(255))
    company_country = db.Column(db.String(255))
    company_office_contact_num = db.Column(db.String(15), nullable=False)
    company_last_contact_time = db.Column(db.TIMESTAMP)
    is_hide = db.Column(db.Boolean, nullable=False, server_default=expression.false())

    company_industry = db.relationship('IndustryArea', backref="company")
    employees = db.relationship('Employee', secondary=t_company_contact, backref="company")

    def __init__(self, company_reg_num, company_name, company_size, company_industry_id, company_desc,
                 company_office_contact_num):
        super().__init__()
        self.company_reg_num = company_reg_num
        self.company_name = company_name
        self.company_size = company_size
        self.company_industry_id = company_industry_id
        self.company_desc = company_desc
        self.company_office_contact_num = company_office_contact_num

    @classmethod
    def create_with_address(cls, company_reg_num, company_name, company_size, company_industry_id, company_desc,
                            company_address
                            , company_postcode, company_city, company_state, company_country,
                            company_office_contact_num):
        company = cls(company_reg_num, company_name, company_size, company_industry_id, company_desc,
                      company_office_contact_num)
        company.company_address = company_address
        company.company_postcode = company_postcode
        company.company_city = company_city
        company.company_state = company_state
        company.company_country = company_country
        return company

    @staticmethod
    def get_all():
        return Company.query.filter_by(is_hide=False).all()
