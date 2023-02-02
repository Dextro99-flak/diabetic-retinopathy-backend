import pathlib
import connexion
from flask_sqlalchemy import SQLAlchemy
import os
from flask import LoginManager
from flask_login import UserMixin

basedir = pathlib.Path(__file__).parent.resolve()
connex_app = connexion.App(__name__, specification_dir=basedir)

app = connex_app.app
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{basedir}/analysis.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'you will never guess ha ha'  #for user login

login=LoginManager(app)
db = SQLAlchemy(app)

class Analysis(db.Model):
	__tablename__='analysis'
	patient_id = db.Column(db.String, primary_key=True)
	image_filename = db.Column(db.String, nullable=False)
	grade = db.Column(db.Integer, nullable=True)
	he_filename = db.Column(db.String, nullable=True)
	ex_filename = db.Column(db.String, nullable=True)
	se_filename = db.Column(db.String, nullable=True)
	ma_filename = db.Column(db.String, nullable=True)
	user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

class User(UserMixin, db.Model):   
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(64),index=True,unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))

	def __repr__(self):
		return '<user: {}>'.format(self.username)

@login.user_loader
def load_user(id):
	return User.query.get(int(id))