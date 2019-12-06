from app import db
from app.models.ModelOperation import ModelOperation


class CompanyEmailStat(ModelOperation, db.Model):
    __tablename__ = 'company_email_stat'

    comp_email_id = db.Column(db.Integer, primary_key=True, unique=True)
    comp_user_id = db.Column(db.ForeignKey('user.user_id'), nullable=False, index=True)
    comp_comp_id = db.Column(db.ForeignKey('company.company_reg_nun'), nullable=False, index=True)
    comp_open_time = db.Column(db.TIMESTAMP)
    comp_sum_open = db.Column(db.Integer, nullable=False)
    comp_status_id = db.Column(db.ForeignKey('email_status.status_id'), nullable=False, index=True)

    comp_comp = db.relationship('Company', backref="company_email_stat")
    comp_status = db.relationship('EmailStatus', backref="company_email_stat")
    comp_user = db.relationship('User', backref="company_email_stat")

    @staticmethod
    def get_all():
        return CompanyEmailStat.query.all()

# # class below is to jsonify the model
# class CompEmailStatSchema(ma.ModelSchema):
#     class Meta:
#         model = CompanyEmailStat
#         # if want return specific fields only :  fields = ('id', 'full_name')
