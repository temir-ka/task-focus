from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_active(self):
        return self.active

    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False
    

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)  # Дата создания задачи
    deadline = db.Column(db.DateTime, nullable=True)  # Дата окончания задачи
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

