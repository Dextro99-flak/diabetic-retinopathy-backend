import pathlib
import connexion
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
import os
from flask_login import UserMixin,LoginManager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_migrate import Migrate


basedir = pathlib.Path(__file__).parent.resolve()
connex_app = connexion.App(__name__, specification_dir=basedir)

app = connex_app.app
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{basedir/'analysis.db'}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'you will never guess ha ha'  #for user login

convention = {
  "ix": "ix_%(column_0_label)s",
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

login=LoginManager(app)
login.login_view = 'login'
db = SQLAlchemy(app,metadata=metadata)
migrate = Migrate(app,db)


class Patient(db.Model): # Add more details to this column as needed
	__tablename__='patient'
	patient_id=db.Column(db.String, primary_key=True)
	name=db.Column(db.String, nullable=False)
	contact=db.Column(db.String, nullable=False)
	address=db.Column(db.String, nullable=True)

class Analysis(db.Model):
	__tablename__='analysis'
	patient_id = db.Column(db.String, db.ForeignKey(Patient.patient_id, ondelete='CASCADE', onupdate='CASCADE'),primary_key=True)
	date_analysed = db.Column(db.String, primary_key=True)
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
	analysis = db.relationship('Analysis',backref='author',lazy='dynamic')

	def __repr__(self):
		return '<user: {}>'.format(self.username)
	
	def set_password(self,password):
		self.password_hash=generate_password_hash(password)
	
	def check_password(self,password):
		return check_password_hash(self.password_hash,password)
with app.app_context():
	db.create_all()
@login.user_loader
def load_user(id):
	return User.query.get(int(id))

