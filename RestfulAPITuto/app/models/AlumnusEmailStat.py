from app import db
from app.models.ModelOperation import ModelOperation


class AlumnusEmailStat(ModelOperation, db.Model):
    __tablename__ = 'alumnus_email_stat'

    alu_email_id = db.Column(db.Integer, primary_key=True, unique=True)
    alu_user_id = db.Column(db.ForeignKey('user.user_id'), nullable=False, index=True)
    alu_alumnus_id = db.Column(db.ForeignKey('employee.employee_id'), nullable=False, index=True)
    alu_open_time = db.Column(db.TIMESTAMP)
    alu_sum_open = db.Column(db.Integer, nullable=False)
    alu_status_id = db.Column(db.ForeignKey('email_status.status_id'), nullable=False, index=True)

    alu_alumnus = db.relationship('Employee', backref="alumnus_email_stat")
    alu_status = db.relationship('EmailStatus', backref="alumnus_email_stat")
    alu_user = db.relationship('User', backref="alumnus_email_stat")

    @staticmethod
    def get_all():
        return AlumnusEmailStat.query.all()

# class AlumnusEmailStatSchema(ma.ModelSchema):
#     class Meta:
#         model = AlumnusEmailStat
#         # if want return specific fields only :  fields = ('id', 'full_name')
