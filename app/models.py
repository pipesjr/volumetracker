from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class Meso(db.Model):
	__tablename__ = 'meso'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True)
	num_of_sessions = db.Column(db.Integer, index=True)
	meso_length = db.Column(db.Integer, index=True)
	session_id= db.Column(db.Integer, index=True, unique=True)
	user_id =db.Column(db.Integer, db.ForeignKey('users.id'))


class SessionData(db.Model):
	__tablename__ = 'sessiondata'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True,unique=True)
	date = db.Column(db.String(64), index=True,unique=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	#meso_id = db.Column(db.Integer, db.ForeignKey('meso.id'))
	#meso = db.relationship(
    #    'Meso',
     #   backref=db.backref('meso', lazy='dynamic', collection_class=list)
    #)
class SessionExercise(db.Model):

	__tablename__ = 'sessionexercise'

	id = db.Column(db.Integer, primary_key=True)

	exercise = db.Column(db.String(64), index=True)
	set = db.Column(db.Integer, index=True)
	rep = db.Column(db.Integer, index=True)
	weight = db.Column(db.Float, index=True)
	session_id = db.Column(db.Integer, db.ForeignKey('sessiondata.id'))
	session = db.relationship(
        'SessionData',
        backref=db.backref('session', lazy='dynamic', collection_class=list)
    )

class Session(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True,unique=True)
	date = db.Column(db.String(64), index=True,unique=True)
	exercise = db.Column(db.String(64), index=True,unique=True)
	set = db.Column(db.Integer, index=True)
	rep = db.Column(db.Integer, index=True)
	weight = db.Column(db.Float, index=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True,unique=True)
    email = db.Column(db.String(120),index=True,unique=True)
    password_hash = db.Column(db.String(128))
    exercise = db.relationship('Exercise', backref='users', lazy='dynamic')
    session = db.relationship('Session', backref='users', lazy='dynamic')



    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
class Exercise(db.Model):
	__tablename__ = 'exercises'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True)

	traps = db.Column(db.Float, index=True)
	front_delts = db.Column(db.Float, index=True)
	side_delts =  db.Column(db.Float, index=True)
	rear_delts = db.Column(db.Float, index=True)
	chest = db.Column(db.Float, index=True)
	back = db.Column(db.Float, index=True)
	biceps = db.Column(db.Float, index=True)
	triceps = db.Column(db.Float, index=True)
	forearms = db.Column(db.Float, index=True)
	abs = db.Column(db.Float, index=True)
	quads = db.Column(db.Float, index=True)
	hams = db.Column(db.Float, index=True)
	glutes = db.Column(db.Float, index=True)
	calves = db.Column(db.Float, index=True)

	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


@login.user_loader
def load_user(id):
	return User.query.get(int(id))