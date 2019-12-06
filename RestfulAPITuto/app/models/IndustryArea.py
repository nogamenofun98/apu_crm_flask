from app import db
from app.models.ModelOperation import ModelOperation


class IndustryArea(ModelOperation, db.Model):
    __tablename__ = 'industry_area'

    industry_id = db.Column(db.Integer, primary_key=True, unique=True)
    industry_name = db.Column(db.String(255), nullable=False)

    @staticmethod
    def get_all():
        return IndustryArea.query.all()

# class below is to jsonify the model
# class IndustryAreaSchema(ma.ModelSchema):
#     class Meta:
#         model = IndustryArea
