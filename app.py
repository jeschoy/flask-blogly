"""Blogly application."""

from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Posts, DEFAULT_URL, Tags, PostTag

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
  user.image_url = request.form['image_url'] or DEFAULT_URL

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

@app.route('/posts/<int:post_id>')
def post_page(post_id):
  """To render a page for a post"""
  post = Posts.query.get_or_404(post_id)
  user = User.query.get_or_404(post.user_id)
  return render_template('/posts/content.html', post=post, user=user)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
  """Show post edit page"""
  post = Posts.query.get_or_404(post_id)
  tags = Tags.query.all()
  return render_template('posts/edit.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def update_post(post_id):
  """To submit edited post"""
  post = Posts.query.get_or_404(post_id)

  post.title = request.form['title']
  post.content = request.form['content']
  tag_ids = [int(num) for num in request.form.getlist("tags")]
  post.tags = Tags.query.filter(Tags.id.in_(tag_ids)).all()

  db.session.add(post)
  db.session.commit()

  return redirect(f'/posts/{post_id}')

@app.route('/users/<int:user_id>/new', methods=["GET"])
def new_post_form(user_id):
  """To show form to add new post"""
  user = User.query.get_or_404(user_id)
  tags = Tags.query.all()
  return render_template('posts/new.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/new', methods=["POST"])
def add_new_post(user_id):
  """Adding new post to the database"""
  user = User.query.get_or_404(user_id)
  tag_ids = [int(num) for num in request.form.getlist("tags")]
  tags = Tags.query.filter(Tags.id.in_(tag_ids)).all()
  new_post = Posts(
    title=request.form['title'],
    content=request.form['content'], user=user, tags=tags)

  db.session.add(new_post)
  db.session.commit()

  return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
  """To remove an existing post"""
  post = Posts.query.get_or_404(post_id)
  db.session.delete(post)
  db.session.commit()
  return redirect(f'/users/{post.user_id}')

@app.route('/tags')
def show_tags():
  """Show page of all tags"""
  tags = Tags.query.all()
  return render_template('/tags/tags.html', tags=tags)

@app.route('/tags/new')
def new_tag_form():
  """Show form to add new tag"""
  return render_template('/tags/new.html')

@app.route('/tags/new', methods=["POST"])
def add_tag():
  """Adding new tags to the database"""

  new_tag = Tags(name=request.form['tags'])

  db.session.add(new_tag)
  db.session.commit()

  return redirect('/tags')

@app.route('/tags/<int:tags_id>/edit')
def edit_tag(tags_id):
  """Show tag edit page"""
  tags = Tags.query.get_or_404(tags_id)
  return render_template('tags/edit.html', tags=tags)

@app.route('/tags/<int:tags_id>/edit', methods=["POST"])
def update_tags(tags_id):
  """To submit edited tag"""
  tags = Tags.query.get_or_404(tags_id)

  tags.name = request.form['tags']

  db.session.add(tags)
  db.session.commit()

  return redirect(f'/tags')

@app.route('/tags/<int:tags_id>')
def tags_page(tags_id):
  """To show posts under tags"""
  tags = Tags.query.get_or_404(tags_id)

  return render_template('tags/posts.html', tags=tags)