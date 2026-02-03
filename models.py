from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to profile
    profile = db.relationship('MasterProfile', backref='user', uselist=False, cascade="all, delete-orphan")

class MasterProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    # Storing the complex profile JSON structure
    profile_json = db.Column(db.JSON, nullable=False, default={})
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_description = db.Column(db.Text, nullable=True)
    company_name = db.Column(db.String(100), nullable=True)
    job_title = db.Column(db.String(100), nullable=True)
    match_score = db.Column(db.Float, default=0.0)
    cv_path = db.Column(db.String(255), nullable=True)
    cl_path = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), default='pending') # pending, processing, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
