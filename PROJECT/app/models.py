from app import db, login_manager
from app import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id=db.Column(db.Integer(), primary_key=True)
    username=db.Column(db.String(length=30), nullable=False, unique=True)
    email=db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash=db.Column(db.String(length=60), nullable=False)

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash=bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    
class Resume(db.Model):
    id=db.Column(db.Integer(), primary_key=True)
    username=db.Column(db.String(length=50), nullable=False)
    name=db.Column(db.String(length=50), nullable=False)
    email=db.Column(db.String(length=50))
    phone_no=db.Column(db.String(length=15))
    location=db.Column(db.String(length=50))
    degree=db.Column(db.String(length=50))
    cllg_name=db.Column(db.String(length=50))
    gpa=db.Column(db.String(length=10))
    grad_year=db.Column(db.String(length=10))
    skills=db.Column(db.String)
    courses=db.Column(db.String)
    designation=db.Column(db.String)
    companies=db.Column(db.String)
    experience=db.Column(db.String)
    achievements=db.Column(db.String)
    awards=db.Column(db.String)
    linkedin=db.Column(db.String)
    github=db.Column(db.String)
    projects=db.Column(db.JSON)
    layout_score=db.Column(db.Float)
    layout_tips=db.Column(db.String)
    smart_project_score=db.Column(db.Float)
    project_tips=db.Column(db.String)
    numerical_metrics=db.Column(db.String)
    top_skillset=db.Column(db.JSON)
    rate=db.Column(db.Float)


    