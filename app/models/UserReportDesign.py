from app import db
from app.models.ModelOperation import ModelOperation


class UserReportDesign(ModelOperation, db.Model):
    __tablename__ = 'user_report_design'

    design_id = db.Column(db.Integer, primary_key=True, unique=True)
    design_json = db.Column(db.JSON)
    user_id = db.Column(db.ForeignKey('user.user_id'), nullable=False, index=True)

    user = db.relationship('User', backref="user_report_design")

    @staticmethod
    def get_all():
        return UserReportDesign.query.all()

# class below is to jsonify the model
# class UserReportSchema(ma.ModelSchema):
#     class Meta:
#         model = UserReportDesign
