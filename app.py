"""Blogly application."""

from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SHHHSECRET"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

app.app_context().push()

connect_db(app)
db.create_all()

@app.route("/")
def root():
  """Home page to show users"""
  return redirect('/users')

@app.route('/users')
def show_users():
  """All users page"""
  users = User.query.all()
  return render_template('users/index.html', users=users)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
  """To show the page of editing an existing user"""
  user = User.query.get_or_404(user_id)
  return render_template('users/edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_edit(user_id):
  """To update the user based off inputs"""
  user = User.query.get_or_404(user_id)

  user.first_name = request.form['first_name']
  user.last_name = request.form['last_name']
  user.image_url = request.form['image_url']

  db.session.add(user)
  db.session.commit() 

  return redirect(f"/users/{user_id}")

@app.route('/users/<int:user_id>')
def user_details(user_id):
  """To show details of each user"""
  user = User.query.get_or_404(user_id)
  return render_template('users/details.html', user=user)

@app.route('/users/new', methods=["GET"])
def user_form():
  """Show form to add a new user"""
  return render_template('users/new.html')

@app.route('/users/new', methods=["POST"])
def add_user():
  """Adding new user to the database"""
  new_user = User(
    first_name=request.form['first_name'], 
    last_name=request.form['last_name'], 
    image_url=request.form['image_url'] or None)

  db.session.add(new_user)
  db.session.commit()

  return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
  """To remove an existing user"""
  user = User.query.get_or_404(user_id)
  db.session.delete(user)
  db.session.commit()
  return redirect('/users')