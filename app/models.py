from app import db

class Character(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)    # Replace with your actual table name
    character = db.Column(db.Text, nullable=False)  # Match the actual column name
    name = db.Column(db.Text)  # Match the actual column name
    img = db.Column(db.Text)


class Norsemen_Characters(db.Model):
	__tablename__ = 'norsemen_characters'  # Replace with your actual table name
	id = db.Column(db.Integer, primary_key=True)
	character_name = db.Column(db.Text, nullable=False)  # Match the actual column name
	description = db.Column(db.Text)  # Match the actual column name
	image_url = db.Column(db.Text)

class Viking_Players(db.Model):
    __tablename__ = 'viking_players'  # Replace with the actual table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    stats = db.Column(db.String, nullable=False)
    photo = db.Column(db.String, nullable=False)
    biography = db.Column(db.String, nullable=False)