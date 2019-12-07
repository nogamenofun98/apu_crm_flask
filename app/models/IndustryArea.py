from app import db
from app.models.ModelOperation import ModelOperation


class IndustryArea(ModelOperation, db.Model):
    __tablename__ = 'industry_area'

    industry_id = db.Column(db.Integer, primary_key=True, unique=True)
    industry_name = db.Column(db.String(255), nullable=False)
    industry_desc = db.Column(db.String(255))

    def __init__(self, industry_name, industry_desc) -> None:
        super().__init__()
        self.industry_name = industry_name
        self.industry_desc = industry_desc

    @staticmethod
    def get_all():
        return IndustryArea.query.all()

# class below is to jsonify the model
# class IndustryAreaSchema(ma.ModelSchema):
#     class Meta:
#         model = IndustryArea
