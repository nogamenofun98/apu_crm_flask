from app import db
from app.models.ModelOperation import ModelOperation


class User(ModelOperation, db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    user_full_name = db.Column(db.String(255), nullable=False)
    user_email = db.Column(db.String(255), nullable=False, unique=True)
    user_role_id = db.Column(db.ForeignKey('user_role.user_role_id'), nullable=True, index=True)
    user_handle_industry_id = db.Column(db.ForeignKey('industry_area.industry_id'), nullable=True, index=True)
    user_handle_industry = db.relationship('IndustryArea', backref="users")
    user_role = db.relationship('UserRole', backref="users")

    def __init__(self, username, user_full_name, user_email) -> None:
        super().__init__()
        self.username = username
        self.user_full_name = user_full_name
        self.user_email = user_email

    @staticmethod
    def get_all():
        return User.query.all()

# # class below is to jsonify the model
# class UserSchema(ma.ModelSchema):
#     class Meta:
#         model = User
# if want return specific fields only :  fields = ('id', 'full_name')
