from app.models.UserRole import UserRole


class UserRoleController:

    @staticmethod
    def get_items():
        return UserRole.get_all()

    @staticmethod
    def create_item(desc, role_json):
        new = UserRole(user_role_description=desc, user_role_json=role_json)
        return new.save()

    @staticmethod
    def find_by_id(item_id):
        return UserRole.query.get(item_id)
