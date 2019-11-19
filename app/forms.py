from flask_wtf import FlaskForm
from wtforms import  Form, FormField, FieldList, StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField,IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User, Exercise
from flask_login import current_user

class MesocycleForm(FlaskForm):
	name = StringField('Mesocycle Name', [DataRequired(message=('Must name mesocycle'))])
	length = SelectField('Length (weeks)', choices=[(1,'1'), (2,'2'), (3,'3'),(4,'4'),(5,'5'), (6,'6'), (7, '7'),
		(8,'8')])
	nums = SelectField('Sessions per week', choices=[(1,'1'), (2,'2'), (3,'3'),(4,'4'),(5,'5'), (6,'6'), (7, '7'),
		(8,'8')])
	submit = SubmitField('Create Mesocycle')

class SessionExerciseForm(Form):
	exercise = SelectField('Exercise', choices=[])
	set = SelectField('Sets', choices=[(1,'1'), (2,'2'), (3,'3'),(4,'4'),(5,'5')])
	rep = IntegerField('Reps')
	weight = IntegerField('Weight')

class SessionForm(FlaskForm):
	name = StringField('Session Name', [DataRequired(message=('Must title exercise'))])
	date = DateField('Date', format='%Y-%m-%d')

	sessionexercise = FieldList(FormField(SessionExerciseForm),
		min_entries=1,
		max_entries=50
		)
	submit = SubmitField('Add Session')



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class ExerciseForm(FlaskForm):
	name = StringField('Exercise  Title', [DataRequired(message=('Must title exercise'))])
	traps = SelectField('Traps', choices=[(0,'0'), (.25, '.25'), (.5, '.5'), (.75, '.75'), (1,'1')])
	front_delts = SelectField('Front Delts', choices=[(0,'0'), (.25, '.25'), (.5, '.5'), (.75, '.75'), (1,'1')])
	side_delts = SelectField('Side Delts', choices=[(0,'0'), (.25, '.25'), (.5, '.5'), (.75, '.75'), (1,'1')])
	rear_delts = SelectField('Rear Delts', choices=[(0,'0'), (.25, '.25'), (.5, '.5'), (.75, '.75'), (1,'1')])
	chest = SelectField('Chest', choices=[(0,'0'), (.25, '.25'), (.5, '.5'), (.75, '.75'), (1,'1')])
	triceps = SelectField('Triceps', choices=[(0,'0'), (.25, '.25'), (.5, '.5'), (.75, '.75'), (1,'1')])
	biceps = SelectField('Biceps', choices=[(0,'0'), (.25, '.25'), (.5, '.5'), (.75, '.75'), (1,'1')])
	forearms = SelectField('Forearms', choices=[(0,'0'), (.25, '.25'), (.5, '.5'), (.75, '.75'), (1,'1')])
	abs = SelectField('Abs', choices=[(0,'0'), (.25, '.25'), (.5, '.5'), (.75, '.75'), (1,'1')])
	back = SelectField('Back', choices=[(0,'0'), (.25, '.25'), (.5, '.5'), (.75, '.75'), (1,'1')])
	glutes = SelectField('Glutes', choices=[(0,'0'), (.25, '.25'), (.5, '.5'), (.75, '.75'), (1,'1')])
	quads = SelectField('Quads', choices=[(0,'0'), (.25, '.25'), (.5, '.5'), (.75, '.75'), (1,'1')])
	hams = SelectField('Hams', choices=[(0,'0'), (.25, '.25'), (.5, '.5'), (.75, '.75'), (1,'1')])
	calves = SelectField('Calves', choices=[(0,'0'), (.25, '.25'), (.5, '.5'), (.75, '.75'), (1,'1')])
	submit = SubmitField('Create Exercise')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
