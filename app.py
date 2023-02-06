from flask import render_template,flash,redirect,url_for,request
import config
from forms import LoginForm
from flask_login import current_user,login_user,logout_user,login_required
from config import User,Analysis,db
from werkzeug.urls import url_parse


#app = Flask(__name__)

app = config.connex_app
app.add_api(config.basedir/'swagger.yml')
application = app.app

@app.route('/')
def home():
	print(current_user)
	return render_template('home.html')

@app.route('/login',methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form=LoginForm()
	if form.validate_on_submit():
		user=User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page=url_for('home')
		return redirect((next_page))
	return render_template('login.html',title='Sign In', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home'))

@app.route('/detector')
@login_required
def detector():
	return render_template('detector.html')



#makes interacting with db from shell easier
#@app.shell_context_processor
#def make_shell_context():
#	return {'db': db,'User':User,'Analysis':Analysis}

if __name__=='__main__':
	app.run( debug=True)

