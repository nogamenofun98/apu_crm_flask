import datetime
import re

from app.models.Employee import Employee
from app.models.EmployeeCompany import EmployeeCompany


class EmployeeController:

    @staticmethod
    def get_columns_name():
        return Employee.__table__.columns.keys()

    @staticmethod
    def get_unassigned_employees(industry_area):
        from app import db
        if industry_area is None:
            return []
        if industry_area.is_read_only and industry_area.industry_name == "All":
            return db.session.query(Employee).filter_by(
                is_hide=False).outerjoin(EmployeeCompany,
                                         Employee.employee_id == EmployeeCompany.alumnus_id).filter_by(
                alumnus_id=None).all()
        else:
            area_id = industry_area.industry_id
            return db.session.query(Employee).filter_by(
                employee_industry_id=area_id, is_hide=False).outerjoin(EmployeeCompany,
                                                                       Employee.employee_id == EmployeeCompany.alumnus_id).filter_by(
                alumnus_id=None).all()

    @staticmethod
    def get_items(industry_area):
        if industry_area is None:
            return []
        if industry_area.is_read_only and industry_area.industry_name == "All":
            return Employee.get_all()
        else:
            area_id = industry_area.industry_id
            return Employee.query.filter_by(employee_industry_id=area_id, is_hide=False).all()

    # @staticmethod
    # def exports(industry_area):
    #     print("exporting")
    #     from app import db
    #     if industry_area.is_read_only and industry_area.industry_name == "All":
    #         return db.session.query(Employee, EmployeeCompany).filter_by(
    #             is_hide=False).outerjoin(EmployeeCompany,
    #                                      Employee.employee_id == EmployeeCompany.alumnus_id).all()
    #     else:
    #         area_id = industry_area.industry_id
    #         return db.session.query(Employee, EmployeeCompany).filter_by(
    #             is_hide=False).outerjoin(EmployeeCompany,
    #                                      Employee.employee_id == EmployeeCompany.alumnus_id).all()

    @staticmethod
    def get_jobs(employee_id):
        return EmployeeCompany.query.filter_by(alumnus_id=employee_id).all()

    @staticmethod
    def find_job(employee_id, company_id):
        return EmployeeCompany.query.filter_by(alumnus_id=employee_id, company_id=company_id).first()

    @staticmethod
    def create_item(employee_full_name, employee_industry_id, employee_alumnus, employee_address='',
                    employee_postcode='', employee_city=''
                    , employee_state='', employee_country='', employee_contact_num='', employee_email='',
                    employee_intake_code='', employee_grad_time=''):

        new = None
        is_error = False
        error_message = ""
        #  check the company is under emp area or not
        # from app.models.Company import Company
        # company = Company.query.filter_by(company_reg_num=employee_current_company_Id, is_hide=False).first()
        # if not company.company_industry_id == employee_industry_id:
        #     is_error = True
        #     error_message += "Working company must same as employee's industry area"
        if employee_full_name.strip() == '':
            is_error = True
            if error_message is not "":
                error_message += ", "
            error_message += "Must provide full name"
        if not type(employee_alumnus) == bool:
            is_error = True
            if error_message is not "":
                error_message += ", "
            error_message += "Must set is APU alumnus or not"

        if not employee_contact_num.strip() == '':
            if not re.match('^(\\+?6?0)[0-9]{1,2}-*[0-9]{7,8}$', str(employee_contact_num)):
                is_error = True
                if error_message is not "":
                    error_message += ", "
                error_message += "Contact number must be in correct format! Received value: " + str(
                    employee_contact_num)

        if not employee_postcode.strip() == '':
            if not re.match('^[0-9]{1,6}$', str(employee_postcode)):
                is_error = True
                if error_message is not "":
                    error_message += ", "
                error_message += "Postcode must be in correct format! Received value: " + str(employee_postcode)
        if not str(employee_grad_time).strip() == "":
            try:
                datetime.datetime.strptime(employee_grad_time, '%Y-%m-%d')
            except ValueError as ex:
                is_error = True
                if error_message is not "":
                    error_message += ", "
                error_message += "Graduation Date format error: " + str(employee_grad_time)

        if not is_error:
            new = Employee(employee_full_name=employee_full_name.strip(),
                           employee_alumnus=employee_alumnus)
            if not employee_address.strip() == "":
                new.employee_address = employee_address
            if not employee_industry_id == "":
                new.employee_industry_id = employee_industry_id
            if not employee_postcode.strip() == "":
                new.employee_postcode = employee_postcode
            if not employee_city.strip() == "":
                new.employee_city = employee_city
            if not employee_state.strip() == "":
                new.employee_state = employee_state
            if not employee_country.strip() == "":
                new.employee_country = employee_country
            if not employee_contact_num.strip() == "":
                new.employee_contact_num = employee_contact_num
            if not employee_grad_time.strip() == "":
                new.employee_grad_time = employee_grad_time
            if not employee_email.strip() == "":
                new.employee_email = employee_email
            if not employee_intake_code.strip() == "":
                new.employee_intake_code = employee_intake_code
            # if not employee_current_company_Id.strip() == "":
            #     new.employee_current_company_Id = employee_current_company_Id
            return new.save()
        else:
            return error_message

    @staticmethod
    def add_working_job(employee_id, company_id, designation, department, hired_time, isCurrentJob=False):
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        # detect if got same emp_id and comp_id in db first, if got, then update it directly
        existing = EmployeeController.find_job(employee_id, company_id)
        if existing is not None:
            # update the record
            if not designation.strip() == "":
                existing.designation = designation
            if not department.strip() == "":
                existing.department = department
            if not hired_time.strip() == "":
                existing.hired_time = hired_time
            existing.updated_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            existing.is_current_job = isCurrentJob
            return existing.commit()
        new = EmployeeCompany(employee_id, company_id)
        if not designation.strip() == "":
            new.designation = designation
        if not department.strip() == "":
            new.department = department
        if not hired_time.strip() == "":
            new.hired_time = hired_time
        new.updated_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new.is_current_job = isCurrentJob
        return new.save()

    @staticmethod
    def find_by_id(item_id):
        return Employee.query.filter_by(employee_id=item_id, is_hide=False).first()

    @staticmethod
    def find_by_contact(email):
        return Employee.query.filter_by(employee_email=email, is_hide=False).first()
