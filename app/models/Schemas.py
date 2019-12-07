from app import ma
from app.models.AlumnusEmailStat import AlumnusEmailStat
from app.models.Company import Company
from app.models.CompanyEmailStat import CompanyEmailStat
from app.models.EmailStatus import EmailStatus
from app.models.Employee import Employee
from app.models.EmployeeCompany import EmployeeCompany
from app.models.IndustryArea import IndustryArea
from app.models.User import User
from app.models.UserReportDesign import UserReportDesign
from app.models.UserRole import UserRole


class AlumnusEmailStatSchema(ma.ModelSchema):
    class Meta:
        model = AlumnusEmailStat


class CompanySchema(ma.ModelSchema):
    class Meta:
        model = Company


class CompEmailStatSchema(ma.ModelSchema):
    class Meta:
        model = CompanyEmailStat


class EmailStatusSchema(ma.ModelSchema):
    class Meta:
        model = EmailStatus


class EmployeeSchema(ma.ModelSchema):
    class Meta:
        model = Employee


class EmpCompSchema(ma.ModelSchema):
    class Meta:
        model = EmployeeCompany


class IndustryAreaSchema(ma.ModelSchema):
    class Meta:
        model = IndustryArea


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        # fields = ('user_id', 'username', 'user_full_name', 'user_email', 'user_role', 'user_handle_industry_id')
        # user_role = ma.Nested("UserRoleSchema")
        # faild to nested schema the Role model into the User model when dump out, maybe try ask CTI


class UserReportSchema(ma.ModelSchema):
    class Meta:
        model = UserReportDesign


class UserRoleSchema(ma.ModelSchema):
    class Meta:
        model = UserRole
