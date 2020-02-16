import re

from app.models.Company import Company


class CompanyController:

    @staticmethod
    def get_columns_name():
        return Company.__table__.columns.keys()

    @staticmethod
    def get_items(industry_area):
        if industry_area.is_read_only and industry_area.industry_name == "All":
            return Company.get_all()
        else:
            area_id = industry_area.industry_id
            return Company.query.filter_by(company_industry_id=area_id, is_hide=False).all()

    @staticmethod
    def create_item(company_reg_num, company_name, company_size, company_industry_id, company_desc,
                    company_office_contact_num, company_address=''
                    , company_postcode='', company_city='', company_state='', company_country=''):
        print(company_reg_num, company_name, company_size, company_industry_id, company_desc,
              company_office_contact_num, company_address
              , company_postcode, company_city, company_state, company_country)
        new = None
        is_error = False
        error_message = ""
        item = CompanyController.find_by_id(company_reg_num)
        if item is not None:
            is_error = True
            error_message += "Registration number duplicated! Received value: " + str(
                company_reg_num)

        if not re.match('^(\\+?6?0)[0-9]{1,2}-*[0-9]{7,8}$', str(company_office_contact_num)):
            is_error = True
            error_message += "Contact number must be in correct format! Received value: " + str(
                company_office_contact_num)

        if not company_address == '':
            if not re.match('^[0-9]{1,6}$', str(company_postcode)):
                is_error = True
                if error_message is not "":
                    error_message += ", "
                error_message += "Postcode must be in correct format! Received value: " + str(company_postcode)

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
        return Company.query.filter_by(company_reg_num=item_id, is_hide=False).first()

    @staticmethod
    def contact_action(company, employee, action):
        from sqlalchemy.exc import SQLAlchemyError
        from app import db
        try:
            if action == 'add':
                company.contacts.append(employee)
                db.session.commit()
                return "Added Contact"  # if no error occurred
            elif action == 'delete':
                company.contacts.remove(employee)
                db.session.commit()
                return "Deleted Contact"  # if no error occurred
        except SQLAlchemyError as ex:
            db.session.rollback()
            from app import config
            if config.Config.DEBUG:
                import re
                return re.sub('[()"]', "", str(ex.__dict__['orig']))
            else:
                return "Error occurred, please contact technical personnel!"
