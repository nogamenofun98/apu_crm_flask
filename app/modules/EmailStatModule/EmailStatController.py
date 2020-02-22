from app.models.AlumnusEmailStat import AlumnusEmailStat
from app.models.CompanyEmailStat import CompanyEmailStat


class EmailStatController:

    @staticmethod
    def get_items(source, industry_area):
        # print("get conversation")
        if industry_area.is_read_only and industry_area.industry_name == "All":
            print("is all")
            if source == "employee":
                return AlumnusEmailStat.get_all()
            else:
                return CompanyEmailStat.get_all()
        else:
            print("is individual")
            area_id = industry_area.industry_id
            if source == "employee":
                return AlumnusEmailStat.query.join("alu_alumnus").filter_by(employee_industry_id=area_id).all()
            else:
                return CompanyEmailStat.query.join("comp_comp").filter_by(company_industry_id=area_id).all()

    @staticmethod
    def create_item(source, user_id, target_id, conversation, status):
        import datetime
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if source == "employee":
            new = AlumnusEmailStat(user_id, target_id, conversation, status, time, time)
        else:
            new = CompanyEmailStat(user_id, target_id, conversation, status, time, time)
        return new.save()

    @staticmethod
    def find_by_id(source, item_id):
        print("find")
        if source == "employee":
            return AlumnusEmailStat.query.filter_by(alu_email_id=item_id).first()
        else:
            return CompanyEmailStat.query.filter_by(comp_email_id=item_id).first()

# @staticmethod
# def add_stat(open_time):
#     print("update open time and plus one")
#
# @staticmethod
# def update_conversation():
#     print("update conversation")
