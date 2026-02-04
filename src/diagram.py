from app import app, db
from models import User, Post, Comment, Follower

with app.app_context():
    db.create_all()