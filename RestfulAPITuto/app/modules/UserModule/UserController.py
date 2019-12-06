from app.models.User import User


class UserController:

    @staticmethod
    def get_users():
        return User.get_all()

    @staticmethod
    def create_user(username, user_full_name, user_email):
        new_user = User(username=username, user_full_name=user_full_name, user_email=user_email)
        return new_user.save()

    @staticmethod
    def find_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def find_user_by_username(username):
        return User.query.filter_by(username=username).first()
