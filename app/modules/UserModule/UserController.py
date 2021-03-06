from app.models.User import User


class UserController:

    @staticmethod
    def get_items():
        return User.get_all()

    @staticmethod
    def create_item(username, user_full_name, user_email):
        new_user = User(username=username, user_full_name=user_full_name, user_email=user_email)
        return new_user.save()

    @staticmethod
    def find_by_id(item_id):
        return User.query.get(item_id)

    @staticmethod
    def find_user_by_username(username):
        return User.query.filter_by(username=username).first()
