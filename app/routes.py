from app import app, db
from flask import render_template,flash, redirect, url_for, request, jsonify
from werkzeug.urls import url_parse
from app.models import User, Exercise, SessionData, SessionExercise, Meso
from flask_login import current_user, login_user, logout_user, login_required
from flask_bootstrap import Bootstrap
from app.forms import LoginForm, RegistrationForm, ExerciseForm, SessionForm, SessionExerciseForm, MesocycleForm
from app.plots import *
from collections import OrderedDict 

db.init_app(app)
db.create_all(app=app)

@app.route('/', methods=["GET", "POST"])
def index():
	return render_template('home.html')
@app.route('/analyze')
@login_required
def analyzer():
	#print(graphing)
	query= db.session.query(Meso.name.distinct())
	mesos = [x[0] for x in query.all()]
	graphing =None
	sessions= SessionData.query.filter_by(user_id=current_user.id).all()
	print(sessions)
	sessions = [(x.id,x.name) for x in sessions]
	return render_template('index.html',plot=graphing, mesos=mesos,sessions=sessions)

@app.route('/getplot',methods=['GET','POST'])
def getplot():
	conn = sqlite3.connect('/Users/peterpeluso/Desktop/flask_rp/app.db')
	cur = conn.cursor()

	df = get_user_exercises(current_user.id, conn)
	exercise_dict = create_exercise_dict(df)
	selected = request.args['selected']
	num_of_sessions, weeks = get_meso_lengths(selected, cur)
	print(num_of_sessions, weeks)
	sessions_in_meso = get_session_ids_in_meso(selected, cur)
	athlete = Athlete()
	athlete.add_exercise_dict(exercise_dict)
	add_sessions_to_athlete_by_session_id(sessions_in_meso, athlete, conn)
	sessions_in_meso = [x.name for x in athlete.sessions]
	athlete.magic()
	meso_data = create_data_for_meso_plot(athlete, num_of_sessions, weeks)
	(plot_session(athlete))
	meso_line_data = create_data_for_meso_line(meso_data)
	graphing = athlete.plots_session_bar[0]
#graphing = plot_meso_weeks_bar(meso_data)[0]
	graphing = plot_meso_line(meso_line_data)
	cur.close()
	conn.close()

	print('here',request.args['selected'])
	#return jsonify(request.args['selected'])
	return graphing

@app.route('/get-sessions',methods=['GET','POST'])
def getsessions():
	conn = sqlite3.connect('/Users/peterpeluso/Desktop/flask_rp/app.db')
	cur = conn.cursor()
	selected = [request.args['selected']]
	print('get session in meso')
	df = get_user_exercises(current_user.id, conn)
	exercise_dict = create_exercise_dict(df)
	#get_meso_lengths('jackeytan', cur)
	athlete = Athlete()
	athlete.add_exercise_dict(exercise_dict)
	add_sessions_to_athlete_by_session_id(selected, athlete, conn)
	athlete.magic()
	plot_session(athlete)
	cur.close()
	conn.close()
	return athlete.plots_session_bar[0]

@app.route('/session-table', methods=['GET', 'POST'])
def sessiontable():
	selected = request.args['selected']
	exercises = SessionExercise.query.filter_by(session_id=selected).all()
	data = []
	for exercise in exercises:
		data.append({'name':exercise.exercise, 'sets': exercise.set,
			'reps': exercise.rep, 'weight': exercise.weight})
	return jsonify(data)

@app.route('/getmeso', methods=['GET', 'POST'])
def getmeso():
	selected = request.args['selected']
	mesos = Meso.query.filter_by(name=selected).all()
	sessions_per_week = mesos[0].num_of_sessions
	weeks = mesos[0].meso_length
	session_ids = [x.session_id for x in mesos]
	print(session_ids)
	sessions = OrderedDict()
	week = 0
	for ix, id in enumerate(session_ids):
		session = SessionData.query.filter_by(id=id).all()
		session = session[0]
		session_of_week = (ix % sessions_per_week) + 1
		if session_of_week == 1:
			week = week +1
		sessions[session.name] = {'mesocycle name':selected,'date': session.date, 'week':week, 'session_num':session_of_week}
	return jsonify(sessions)
@app.route('/mesocycle', methods=['GET', 'POST'])
@login_required
def mesocycle():
	form = MesocycleForm()
	if request.method == 'POST':
		chosen = request.form.getlist('sessions')
		if chosen != []:
			for session_id in chosen:
				meso = Meso(name=form.name.data, num_of_sessions= form.nums.data, meso_length=form.length.data,
					session_id= session_id, user_id=current_user.id)
				db.session.add(meso)
			db.session.commit()
	sessions_user = SessionData.query.filter_by(user_id=current_user.id).all()
	sessions_name = [(x.id,x.name) for x in sessions_user]
	return render_template('meso.html',form=form, sessions=sessions_name)

@app.route('/session',methods=['GET', 'POST'])
@login_required
def session():
    form = SessionForm()
    #form.exercise.choices = [(x.name,x.name) for x in Exercise.query.filter_by(user_id=current_user.id).all()]
    if request.method == 'POST':
        session = SessionData(name=form.name.data, date=form.date.data, user_id=current_user.id)
        db.session.add(session)
        for i in form.sessionexercise.data:
        	print(i)
        	x = SessionExercise(exercise=i['exercise'], set=i['set'],rep=i['rep'], weight=i['weight'])
        	session.session.append(x)
        db.session.commit()
    return render_template('session.html',form=form, exs= [(x.name, x.name) for x in Exercise.query.filter_by(user_id=current_user.id).all()])

@app.route('/exercise', methods=['GET', 'POST'])
@login_required
def exercise():
	form = ExerciseForm()
	if request.method == 'POST':
		ex = Exercise(name=form.name.data,traps=form.traps.data,
			front_delts= form.front_delts.data, side_delts = form.side_delts.data,
			rear_delts=form.rear_delts.data, chest=form.chest.data, triceps=form.triceps.data,
			biceps= form.biceps.data, back=form.back.data, abs= form.abs.data, quads=form.quads.data,
			hams=form.hams.data, calves=form.calves.data, glutes=form.glutes.data,forearms= form.forearms.data,user_id=current_user.id)
		db.session.add(ex)
		db.session.commit()
		print(ex.user_id)
	return render_template('exercise.html',form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()

	if form.validate():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None:
			flash('Invalid username or password')
			return redirect(url_for('login'))
		if not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember= form.remember_me.data)
		next_page = request.args.get('next')
		print(next_page)
		if not next_page or url_parse(next_page).netloc != '':
			return redirect(url_for('index'))
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)

@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
