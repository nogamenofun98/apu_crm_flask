from app import db
from app.models.ModelOperation import ModelOperation


class UserRole(ModelOperation, db.Model):
    __tablename__ = 'user_role'

    user_role_id = db.Column(db.Integer, primary_key=True, unique=True)
    user_role_description = db.Column(db.String(255), nullable=False)
    user_role_json = db.Column(db.JSON, nullable=False)

    def __init__(self, user_role_description, user_role_json) -> None:
        super().__init__()
        self.user_role_description = user_role_description
        self.user_role_json = user_role_json

    @staticmethod
    def get_all():
        return UserRole.query.all()

# class below is to jsonify the model
# class UserRoleSchema(ma.ModelSchema):
#     class Meta:
#         model = UserRole
