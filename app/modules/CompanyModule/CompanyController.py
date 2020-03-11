import re

from app.models.Company import Company


class CompanyController:

    @staticmethod
    def get_columns_name():
        return Company.__table__.columns.keys()

    @staticmethod
    def get_items(industry_area):
        if industry_area is None:
            return []
        if industry_area.is_read_only and industry_area.industry_name == "All":
            return Company.get_all()
        else:
            area_id = industry_area.industry_id
            return Company.query.filter_by(company_industry_id=area_id, is_hide=False).all()

    @staticmethod
    def create_item(company_reg_num, company_name, company_size, company_industry_id, company_desc,
                    company_office_contact_num, company_address=''
                    , company_postcode='', company_city='', company_state='', company_country=''):
        new = None
        is_error = False
        error_message = ""
        item = CompanyController.find_by_id(company_reg_num)
        if item is not None:
            is_error = True
            error_message += "Registration number duplicated! Received value: " + str(
                company_reg_num)

        company_reg_num = str(company_reg_num).strip()
        company_name = str(company_name).strip()
        company_size = str(company_size).strip()
        company_desc = str(company_desc).strip()
        if company_reg_num == '':
            return "Registration number cannot be empty!"
        if company_name == '':
            return "Name cannot be empty!"
        if company_size == '':
            return "Size cannot be empty!"
        if company_desc == '':
            return "Description cannot be empty!"

        if not re.match('^(\\+?6?0)[0-9]{1,2}-*[0-9]{7,8}$', str(company_office_contact_num)):
            is_error = True
            error_message += "Contact number must be in correct format! Received value: " + str(
                company_office_contact_num)

        if not company_postcode == '':
            if not re.match('^[0-9]{1,6}$', str(company_postcode)):
                is_error = True
                if error_message is not "":
                    error_message += ", "
                error_message += "Postcode must be in correct format! Received value: " + str(company_postcode)

        if not is_error:
            new = Company(company_reg_num=company_reg_num, company_name=company_name, company_size=company_size,
                          company_industry_id=company_industry_id, company_desc=company_desc,
                          company_office_contact_num=company_office_contact_num)
            if not company_address.strip() == "":
                new.company_address = company_address
            if not company_postcode.strip() == "":
                new.company_postcode = company_postcode
            if not company_city.strip() == "":
                new.company_city = company_city
            if not company_state.strip() == "":
                new.company_state = company_state
            if not company_country.strip() == "":
                new.company_country = company_country
            return new.save()
        else:
            return error_message

    @staticmethod
    def find_by_id(item_id):
        return Company.query.filter_by(company_reg_num=item_id, is_hide=False).first()

    @staticmethod
    def get_employees(item_id):
        from app.models.EmployeeCompany import EmployeeCompany
        from app.models.Employee import Employee
        from app import db
        return db.session.query(Company, EmployeeCompany, Employee).filter(
            Company.company_reg_num == item_id, Company.is_hide == False, Company.company_reg_num == EmployeeCompany.company_id, EmployeeCompany.alumnus_id == Employee.employee_id, EmployeeCompany.is_current_job == True).all()

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
