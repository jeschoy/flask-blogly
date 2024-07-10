"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

# default url for no input of image
DEFAULT_URL = "https://www.shutterstock.com/image-vector/default-avatar-profile-icon-social-600nw-1677509740.jpg"

class User(db.Model):
  """User of the site"""
  __tablename__ = 'users'

  id = db.Column(db.Integer, 
                 primary_key=True)
  first_name = db.Column(db.Text,
                         nullable=False)
  last_name = db.Column(db.Text,
                         nullable=False)
  image_url = db.Column(db.Text,
                        nullable=False, default=DEFAULT_URL)
  
  posts = db.relationship("Posts", backref="user", cascade="all, delete-orphan")

  @property
  def full_name(self):
    """To show full name for user"""
    return f"{self.first_name} {self.last_name}"

class Posts(db.Model):
  """Posts on the website"""
  __tablename__ = 'posts'

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.Text, nullable=False)
  content = db.Column(db.Text, nullable=False)
  created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class PostTag(db.Model):
  """Post tags"""
  __tablename__ = 'post_tags'

  post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
  tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

class Tags(db.Model):
  """Tags that can be used for posts"""
  __tablename__ = 'tags'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.Text, nullable=False, unique=True)

  posts = db.relationship('Posts', secondary='post_tags', backref='tags')


def connect_db(app):
  db.app = app
  db.init_app(app)