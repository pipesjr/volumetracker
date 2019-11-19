import datetime as dt
import pandas as pd
import numpy as np
BODYPARTS = ["Traps", "Front Delts", "Side Delts", "Rear Delts",
			  "Chest", "Triceps", "Biceps", "Forearms", "Abs",
			  "Back", "Glutes", "Quads", "Hams", "Calves"]
class Exercise: 

	def __init__(self, name, bodyparts):
		self.name = name
		self.bodyparts = bodyparts

def create_bodypart_dict(muscle, magnitude):

	return dict(zip(muscle, magnitude))

df = pd.read_csv('parts.csv')
df = df.set_index(df['Exercise'])
exercise_dict = {}
print(df)
import sqlite3
conn = sqlite3.connect("data.db")
cur = conn.cursor()
df = pd.read_sql_query('SELECT * FROM users;',conn)
df = df.set_index(df['Exercise'])
print(df)
#df.to_sql('users', con=conn)
cur.close()
conn.close()


for i in df.index:
	print(i)
	bp = []
	mag = []

	for j in BODYPARTS:
		print(df.ix[i][j])
		if df.ix[i][j] != np.nan:
			bp.append(j)
			mag.append(df.ix[i][j])
		else:
			pass

	exercise_dict[i] = Exercise(i, create_bodypart_dict(bp,mag))


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
	    self.exercises_and_reps[exercise] = reps
	    self.exercises_and_weights[exercise] = weights


class Athlete:
	def __init__(self):
		self.sessions = []
		self.bodyparts = []

	def add_session(self,session):
		self.sessions.append(session)

	def magic(self):
		for ix,k  in enumerate(self.sessions):
			self.bodyparts.append(pd.DataFrame(0,index=np.arange(len([1])),columns=BODYPARTS))
			for i in k.exercises_and_reps:
				sets = len(k.exercises_and_reps[i])
				for j in exercise_dict[i].bodyparts:
					if exercise_dict[i].bodyparts[j] > 0:
						self.bodyparts[ix][j] = self.bodyparts[ix][j][0] + (sets * exercise_dict[i].bodyparts[j])
					else:
						self.bodyparts[ix][j] = self.bodyparts[ix][j][0]

				print(self.bodyparts[ix])