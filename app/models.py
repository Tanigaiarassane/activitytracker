from datetime import datetime
from app import  db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable = False, unique = True)
    email = db.Column(db.String(20), nullable= False, unique = True)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    todo_list = db.relationship('ActivityItem', backref='author', lazy = True)

    def __repr__(self):
        return "User({},{})".format(self.name, self.email,self.todo_list)

class ActivityItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable= False, unique = True)
    content = db.Column(db.Text, nullable = False)
    status = db.Column(db.String(10), nullable = False, default= "New")
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __repr__(self):
        return "ActivityItem({},{},{},{})".format(self.name, self.content,self.status, self.user_id)


class Mathematician(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    hit = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "Mathematician({},{})".format(self.name.encode('utf-8'), self.hit)
