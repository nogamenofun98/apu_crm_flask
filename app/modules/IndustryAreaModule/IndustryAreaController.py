from app.models.IndustryArea import IndustryArea


class IndustryAreaController:

    @staticmethod
    def get_items():
        return IndustryArea.get_all()

    @staticmethod
    def create_item(name, desc):
        new = IndustryArea(industry_name=name, industry_desc=desc)
        return new.save()

    @staticmethod
    def find_by_id(item_id):
        return IndustryArea.query.get(item_id)
