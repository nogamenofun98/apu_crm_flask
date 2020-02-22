from sqlalchemy import text

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
    alu_conversation = db.Column(db.String(4294000000))
    alu_updated_time = db.Column(db.TIMESTAMP)

    alu_alumnus = db.relationship('Employee', backref="alumnus_email_stat")
    alu_status = db.relationship('EmailStatus', backref="alumnus_email_stat")
    alu_user = db.relationship('User', backref="alumnus_email_stat")

    def __init__(self, user_id, target_id, conversation, status_id, open_time, updated_time):
        super().__init__()
        self.alu_user_id = user_id
        self.alu_alumnus_id = target_id
        self.alu_sum_open = 0
        self.alu_status_id = status_id
        self.alu_conversation = conversation
        self.alu_open_time = open_time
        self.alu_updated_time = updated_time

    @staticmethod
    def get_all():
        return AlumnusEmailStat.query.all()

# class AlumnusEmailStatSchema(ma.ModelSchema):
#     class Meta:
#         model = AlumnusEmailStat
#         # if want return specific fields only :  fields = ('id', 'full_name')
