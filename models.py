from app import db


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    steam_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    logo_url = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<Game %r>' % self.steam_id