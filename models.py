"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# default url for no input of image
DEFAULT_URL = "https://www.shutterstock.com/image-vector/default-avatar-profile-icon-social-600nw-1677509740.jpg"

def connect_db(app):
  db.app = app
  db.init_app(app)

class User(db.Model):
  """User of the site"""
  __tablename__ = 'users'

  id = db.Column(db.Integer, 
                 primary_key=True)
  first_name = db.Column(db.Text,
                         nullable=True)
  last_name = db.Column(db.Text,
                         nullable=True)
  image_url = db.Column(db.Text,
                        nullable=False, default=DEFAULT_URL)
  
  @property
  def full_name(self):
    """To show full name for user"""
    return f"{self.first_name} {self.last_name}"
