from flask_login import UserMixin

from config import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    hashed_password = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    # Используйте 'reviews' вместо 'users' для атрибута backref
    reviews = db.relationship('Review', backref='user', secondary='user_reviews')


# Модель Review для хранения информации об отзывах
class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 



user_reviews = db.Table(
    'user_reviews',
    db.Column(
        'user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column(
        'review_id', db.Integer, db.ForeignKey('reviews.id'), primary_key=True),
)

