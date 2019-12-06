from app.models.UserRole import UserRole


class UserRoleController:

    @staticmethod
    def get_roles():
        return UserRole.get_all()

    @staticmethod
    def create_role(desc, role_json):
        new = UserRole(user_role_description=desc, user_role_json=role_json)
        return new.save()

    @staticmethod
    def find_role_by_id(role_id):
        return UserRole.query.get(role_id)
