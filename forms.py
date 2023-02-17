from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField,FileRequired,FileAllowed

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    
class PhotoForm(FlaskForm):
    photo=FileField(validators=[FileRequired(),FileAllowed(['jpg','jpeg'])])
    submit=SubmitField("begin processing")
    patient_name = StringField('Patient Name')
    patient_id = StringField('Patient ID')

class PatientForm(FlaskForm):
    patient_name = StringField('Patient Name')
    patient_id = IntegerField('Patient ID')