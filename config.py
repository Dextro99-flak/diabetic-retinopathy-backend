import pathlib
import connexion
from flask_sqlalchemy import SQLAlchemy

basedir = pathlib.Path(__file__).parent.resolve()
connex_app = connexion.App(__name__, specification_dir=basedir)

app = connex_app.app
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{basedir/'analysis.db'}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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