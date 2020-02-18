from app import db
from app.models.ModelOperation import ModelOperation


class EmailStatus(ModelOperation, db.Model):
    __tablename__ = 'email_status'

    status_id = db.Column(db.Integer, primary_key=True, unique=True)
    status_name = db.Column(db.String(255), nullable=False)
    status_description = db.Column(db.String(255))

    def __init__(self, status_name, status_description):
        super().__init__()
        self.status_name = status_name
        self.status_description = status_description

    @staticmethod
    def get_all():
        return EmailStatus.query.all()

# class below is to jsonify the model
# class EmailStatusSchema(ma.ModelSchema):
#     class Meta:
#         model = EmailStatus
