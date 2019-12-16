from sqlalchemy.sql import expression

from app import db
from app.models.ModelOperation import ModelOperation


class IndustryArea(ModelOperation, db.Model):
    __tablename__ = 'industry_area'

    industry_id = db.Column(db.Integer, primary_key=True, unique=True)
    industry_name = db.Column(db.String(255), nullable=False)
    industry_desc = db.Column(db.String(255))
    is_read_only = db.Column(db.Boolean, nullable=False, server_default=expression.false())

    def __init__(self, industry_name, industry_desc, is_read_only=False) -> None:
        super().__init__()
        self.industry_name = industry_name
        self.industry_desc = industry_desc
        self.is_read_only = is_read_only

    @staticmethod
    def get_all():
        return IndustryArea.query.all()

# class below is to jsonify the model
# class IndustryAreaSchema(ma.ModelSchema):
#     class Meta:
#         model = IndustryArea
