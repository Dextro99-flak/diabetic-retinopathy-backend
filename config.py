import pathlib
import connexion
from flask_sqlalchemy import SQLAlchemy
#import bcrypt

basedir = pathlib.Path(__file__).parent.resolve()
connex_app = connexion.App(__name__, specification_dir=basedir)

app = connex_app.app
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{basedir/'analysis.db'}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Patient(db.Model): # Add more details to this column as needed
	__tablename__='patient'
	patient_id=db.Column(db.String, primary_key=True)
	name=db.Column(db.String, nullable=False)
	contact=db.Column(db.String, nullable=False)
	address=db.Column(db.String, nullable=True)

class Analysis(db.Model):
	__tablename__='analysis'
	patient_id = db.Column(db.String, db.ForeignKey(Patient.patient_id, ondelete='CASCADE', onupdate='CASCADE'),primary_key=True)
	date_analysed = db.Column(db.DateTime, primary_key=True)
	image_filename = db.Column(db.String, nullable=False)
	grade = db.Column(db.Integer, nullable=True)
	he_filename = db.Column(db.String, nullable=True)
	ex_filename = db.Column(db.String, nullable=True)
	se_filename = db.Column(db.String, nullable=True)
	ma_filename = db.Column(db.String, nullable=True)

class User(db.Model):
	__tablename__='user'
	user_id=db.Column(db.String, primary_key=True)
	username=db.Column(db.String, unique=True, nullable=False)
	password=db.Column(db.String, nullable=False)

	# def verify_password_direct(self, password): # Password Hash sent from front end is verified here
	# 	pwhash=bcrypt.hashpw(password,self.password)
	# 	return self.password==pwhash