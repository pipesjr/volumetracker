import plotly
import plotly.graph_objs as go
import sqlite3
import pandas as pd
import numpy as np
import json
import datetime as dt
from app.models import Meso, SessionData

conn = sqlite3.connect('/Users/peterpeluso/Desktop/flask_rp/app.db')
cur = conn.cursor()

df =pd.read_sql_query('select * from exercises;',conn)
df = df.set_index(df['name'])


BODYPARTS = ["Traps", "Front_Delts", "Side_Delts", "Rear_Delts",
			  "Chest", "Triceps", "Biceps", "Forearms", "Abs",
			  "Back", "Glutes", "Quads", "Hams", "Calves"]
BODYPARTS = [x.lower() for x in BODYPARTS]

class ExerciseForPlot: 
	def __init__(self, name, bodyparts):
		self.name = name
		self.bodyparts = bodyparts
	def __str__(self):
		return json.dumps({self.name: self.bodyparts})





class Session:
    def __init__(self,name=None,date=None):
        self.exercises_and_reps = {}
        self.exercises_and_weights = {}
        if name == None:
            self.name = dt.date.today()
        else:
            self.name = name
        if date == None:
            self.date = dt.date.today()
        else:
            self.date = date
    def add_exercise(self, exercise, reps, weights):

        if exercise in self.exercises_and_reps.keys():
            self.exercises_and_reps[exercise] = self.exercises_and_reps[exercise]  + reps
            self.exercises_and_weights[exercise] = self.exercises_and_reps[exercise]  +weights			
        else:
            self.exercises_and_reps[exercise] = reps
            self.exercises_and_weights[exercise] = weights

class Athlete:
	def __init__(self):
		self.sessions = []
		self.bodyparts = []
		self.bodyparts_by_session = {}
		self.plots_session_bar = []
		self.exercise_dict = {}

	def add_session(self,session):
		self.sessions.append(session)
	def add_exercise_dict(self, exs_dict):
		self.exercise_dict = exs_dict
	def magic(self):  # used to calculate sets per bodypart for a session
		for ix,k  in enumerate(self.sessions):
			self.bodyparts.append(pd.DataFrame(0,index=np.arange(len([1])),columns=BODYPARTS))
			for i in k.exercises_and_reps:
				sets = len(k.exercises_and_reps[i])
				for j in self.exercise_dict[i].bodyparts:
					if self.exercise_dict[i].bodyparts[j] > 0:
						print(self.bodyparts[ix][j][0] + (sets * self.exercise_dict[i].bodyparts[j]))
						self.bodyparts[ix][j] = self.bodyparts[ix][j][0] + (sets * self.exercise_dict[i].bodyparts[j])
					else:
						self.bodyparts[ix][j] = self.bodyparts[ix][j][0]

				print(self.bodyparts[ix])

def get_user_exercises(user_id, conn):    # returns df of user exercises
	df =pd.read_sql_query('select * from exercises;',conn)
	df = df.set_index(df['name'])

	return df
def create_bodypart_dict(muscle, magnitude):

	return dict(zip(muscle, magnitude))

def create_exercise_dict(exercises_df):  # arguement is df from exercise db
    exercise_dict = {}
    df = exercises_df
    for i in df.index:
	    print('i= ',i)
	    bp = []
	    mag = []

	    for j in BODYPARTS:
		    j= j.lower()
		    print('j= ',j)
		    print(df.ix[i][j])
		    if df.ix[i][j] != np.nan:
			    bp.append(j)
			    mag.append(df.ix[i][j])
		    else:
			    pass

	    exercise_dict[i] = ExerciseForPlot(i, create_bodypart_dict(bp,mag))
    return exercise_dict

def get_session_ids_in_meso(meso_name, cur):
	cur.execute('select session_id from meso where name= "{}";'.format(meso_name))
	data = cur.fetchall()
	data = [x[0] for x in data]
	return data

def arrs(set, rep, weight):  # takes workout from db and turns to arrs fro Session.add_exercise()
	reps = []
	weights = []
	for i in range(set):
		reps.append(rep)
		weights.append(weight)

	return reps, weights

def add_sessions_to_athlete_by_session_id(sessions_in_meso, athlet, conn): # sessions come as in form of return from get_session_ids_in_meso
    for sessions in sessions_in_meso:
        workout =pd.read_sql_query(' select * from sessionexercise where session_id={};'.format(sessions),conn)
        session_data = SessionData.query.filter_by(id=sessions).first().name
        session = Session(name=session_data)
        for i in workout.index:

            name=workout.ix[i]['exercise']
            reps_arr, weights_arr = arrs(workout.ix[i]['set'], workout.ix[i]['rep'], workout.ix[i]['weight'])
            print(reps_arr)
            print(weights_arr)

            session.add_exercise(name, reps_arr, weights_arr)
        athlet.add_session(session)

def plot_session(athlete):   # plots a bargraph of body parts for each session
    arr = []
    for i in athlete.bodyparts:
        data = [go.Bar(x=i.columns, y=i.ix[0])]
        graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
        arr.append(graphJSON)
    athlete.plots_session_bar = arr

def get_meso_lengths(meso_name,cur):
	data = Meso.query.filter_by(name=meso_name).first()
	print('THIS: ', data)
	return (data.num_of_sessions, data.meso_length)

def create_data_for_meso_plot(athlete, num_ses, length): # adds bodyparts df together by week of mesocycle
	meso_weeks = []
	sesh_num = 0
	for i in range(length):
		df = athlete.bodyparts[sesh_num]
	
		for j in range(num_ses-1):
			sesh_num = sesh_num +1
			df = df + athlete.bodyparts[sesh_num]
		sesh_num = sesh_num +1
		meso_weeks.append(df)
	return meso_weeks
def create_data_for_meso_line(meso_weeks): # takes data from create_data_for_meso_plot and turns it into data for line plot
    df = meso_weeks[0]

    for i in meso_weeks[1:]:

    	df = df.append(i)
    	df = df.reset_index()

    return df
def plot_meso_weeks_bar(meso_data):
    arr = []
    for i in meso_data:
        data = [go.Bar(x=i.columns, y=i.ix[0])]
        fig = go.Figure(data=data)
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        arr.append(graphJSON)
    return arr

def plot_meso_line(meso_data):
    lines = []
    for part in meso_data.columns:
        lines.append(go.Scatter(x=meso_data.index, y=meso_data[part],
                    mode='lines',
                    name=part))
    graphJSON = json.dumps(lines, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

# exercise_dict = create_exercise_dict(df)
# get_meso_lengths('jackeytan', cur)
# sessions_in_meso = get_session_ids_in_meso('jackeytan', cur)
# athlete = Athlete()
# add_sessions_to_athlete_by_session_id(sessions_in_meso, athlete)
# athlete.magic()
# meso_data = create_data_for_meso_plot(athlete, 1,2)
# (plot_session(athlete))
# meso_line_data = create_data_for_meso_line(meso_data)
# graphing = athlete.plots_session_bar[0]
# #graphing = plot_meso_weeks_bar(meso_data)[0]
# graphing = plot_meso_line(meso_line_data)
cur.close()
conn.close()