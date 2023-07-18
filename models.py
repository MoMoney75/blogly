"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import delete, update
db = SQLAlchemy()

Default_image='https://unsplash.com/photos/a-brown-dog-standing-on-top-of-a-wooden-dock-YTvDtPaqknI'
def connect_db(app):
    db.app = app
    db.init_app(app)
    
def __repr__(self):
    u = self
    return f'<Users{u.id} {u.first_name}  {u.last_name} {u.image_url}'
    
class User(db.Model):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text,  nullable=False)
    last_name = db.Column(db.Text,  nullable=False)
    image_url = db.Column(db.Text, unique=False, nullable=True, default=Default_image) 



