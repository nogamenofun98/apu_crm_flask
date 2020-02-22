from app import db
from app.models.AlumnusEmailStat import AlumnusEmailStat
from app.models.CompanyEmailStat import CompanyEmailStat


class DashboardController:

    @staticmethod
    def get_conversations(source):
        print("word cloud")
        if source == "company":
            return db.session.query(CompanyEmailStat.comp_conversation).all()
        else:
            return db.session.query(AlumnusEmailStat.alu_conversation).all()

    @staticmethod
    def get_session():
        return db.session
