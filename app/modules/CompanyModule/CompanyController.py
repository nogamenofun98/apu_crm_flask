import re

from app.models.Company import Company


class CompanyController:

    @staticmethod
    def get_items(industry_area):
        if industry_area.is_read_only and industry_area.industry_name == "All":
            return Company.get_all()
        else:
            area_id = industry_area.industry_id
            return Company.query.filter_by(company_industry_id=area_id).all()

    # company_reg_num = db.Column(db.Integer, primary_key=True, autoincrement=False)
    # company_name = db.Column(db.String(255), nullable=False)
    # company_size = db.Column(db.Integer, nullable=False)
    # company_industry_id = db.Column(db.ForeignKey('industry_area.industry_id'), nullable=False, index=True)
    # company_desc = db.Column(db.String(255), nullable=False)
    # company_address = db.Column(db.Integer, nullable=False)
    # company_postcode = db.Column(db.String(255))
    # company_city = db.Column(db.String(255))
    # company_state = db.Column(db.String(255))
    # company_country = db.Column(db.String(255))
    # company_office_contact_num = db.Column(db.Integer, nullable=False)

    @staticmethod
    def create_item(company_reg_num, company_name, company_size, company_industry_id, company_desc,
                    company_office_contact_num, company_address=''
                    , company_postcode='', company_city='', company_state='', company_country=''):
        # print(company_reg_num, company_name, company_size, company_industry_id, company_desc,
        #       company_office_contact_num, company_address
        #       , company_postcode, company_city, company_state, company_country)
        new = None
        is_error = False
        error_message = ""
        # print(re.match('^(\\+?6?0)[0-9]{1,2}-*[0-9]{7,8}$', company_office_contact_num))
        if not re.match('^(\\+?6?0)[0-9]{1,2}-*[0-9]{7,8}$', company_office_contact_num):
            is_error = True
            error_message += "Company contact number must be in correct format! Received value: " + company_office_contact_num

        if not re.match('^[0-9]{1,6}$', company_postcode):
            is_error = True
            if error_message is not "":
                error_message += ", "
            error_message += "Company postcode must be in correct format! Received value: " + company_postcode

        if not is_error:
            if company_address == '':
                new = Company(company_reg_num=company_reg_num, company_name=company_name, company_size=company_size,
                              company_industry_id=company_industry_id, company_desc=company_desc,
                              company_office_contact_num=company_office_contact_num)
            else:
                new = Company.create_with_address(company_reg_num=company_reg_num, company_name=company_name,
                                                  company_size=company_size, company_industry_id=company_industry_id,
                                                  company_desc=company_desc,
                                                  company_address=company_address
                                                  , company_postcode=company_postcode, company_city=company_city,
                                                  company_state=company_state, company_country=company_country,
                                                  company_office_contact_num=company_office_contact_num)
            # print('Company: ' + new.company_reg_num, new.company_address)
            return new.save()
        else:
            return error_message

    @staticmethod
    def find_by_id(item_id):
        return Company.query.get(item_id)
