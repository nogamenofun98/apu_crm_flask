from sqlalchemy import text

from app import db
from app.models.ModelOperation import ModelOperation


class CompanyEmailStat(ModelOperation, db.Model):
    __tablename__ = 'company_email_stat'

    comp_email_id = db.Column(db.Integer, primary_key=True, unique=True)
    comp_user_id = db.Column(db.ForeignKey('user.user_id'), nullable=False, index=True)
    comp_comp_id = db.Column(db.ForeignKey('company.company_reg_num'), nullable=False, index=True)
    comp_open_time = db.Column(db.TIMESTAMP)
    comp_sum_open = db.Column(db.Integer, nullable=False)
    comp_status_id = db.Column(db.ForeignKey('email_status.status_id'), nullable=False, index=True)
    comp_conversation = db.Column(db.String(4294000000))
    comp_updated_time = db.Column(db.TIMESTAMP)

    comp_comp = db.relationship('Company', backref="company_email_stat")
    comp_status = db.relationship('EmailStatus', backref="company_email_stat")
    comp_user = db.relationship('User', backref="company_email_stat")

    def __init__(self, user_id, target_id, conversation, status_id, open_time, updated_time):
        super().__init__()
        self.comp_user_id = user_id
        self.comp_comp_id = target_id
        self.comp_sum_open = 0
        self.comp_status_id = status_id
        self.comp_conversation = conversation
        self.comp_open_time = open_time
        self.comp_updated_time = updated_time

    @staticmethod
    def get_all():
        return CompanyEmailStat.query.all()

# # class below is to jsonify the model
# class CompEmailStatSchema(ma.ModelSchema):
#     class Meta:
#         model = CompanyEmailStat
#         # if want return specific fields only :  fields = ('id', 'full_name')
