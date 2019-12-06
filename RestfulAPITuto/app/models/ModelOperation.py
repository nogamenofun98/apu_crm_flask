import re

from sqlalchemy.exc import SQLAlchemyError

from app import db, config


class ModelOperation(object):
    # column will define in child class

    def save(self):
        db.session.add(self)
        return self.commit()
        # need to do db message forwarding to json frontend

    def delete(self):
        db.session.delete(self)
        return self.commit()

    def commit(self):
        try:
            db.session.commit()
            return None  # if no error occurred
        except SQLAlchemyError as ex:
            db.session.rollback()
            if config.Config.DEBUG:
                return re.sub('[()"]', "", str(ex.__dict__['orig']))
            else:
                return "Error occurred, please contact technical personnel!"
