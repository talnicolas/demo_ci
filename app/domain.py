from app import db
from app.string_utils import build_connection_string

class Datasource(db.Model):
    __tablename__ = 'datasources'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    connection_string = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, name, driver, host, port, db):
        self.name = name
        self.connection_string = build_connection_string(driver, host, port, db)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Datasource.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Datasource: {}>".format(self.name)