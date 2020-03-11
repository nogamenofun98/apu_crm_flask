from app.models.UserRole import UserRole


class UserRoleController:

    @staticmethod
    def get_items():
        return UserRole.get_all()

    @staticmethod
    def create_item(desc, role_json):
        desc = str(desc).strip()
        # role_json = str(role_json).strip()
        if desc == '':
            return 'Description cannot empty!'
        if role_json == '':
            return 'Role json cannot empty!'
        new = UserRole(user_role_description=desc, user_role_json=role_json)
        return new.save()

    @staticmethod
    def find_by_id(item_id):
        return UserRole.query.get(item_id)
