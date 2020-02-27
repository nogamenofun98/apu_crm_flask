from app.models.IndustryArea import IndustryArea


class IndustryAreaController:

    @staticmethod
    def get_items():
        return IndustryArea.get_all()

    @staticmethod
    def create_item(name, desc, is_read_only=False):
        name = str(name).strip()
        desc = str(desc).strip()
        if name == '':
            return "Name cannot be empty!"
        new = IndustryArea(industry_name=name, industry_desc=desc, is_read_only=is_read_only)
        return new.save()


    @staticmethod
    def find_by_id(item_id):
        return IndustryArea.query.get(item_id)

    @staticmethod
    def get_default_all_area() -> IndustryArea:
        return IndustryArea.query.filter_by(is_read_only=True, industry_name='All').first()
