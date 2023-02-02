from flask import render_template,flash,redirect
import config
from forms import LoginForm

#app = Flask(__name__)

app = config.connex_app
app.add_api(config.basedir/'swagger.yml')

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/login',methods=['GET','POST'])
def login():
	form=LoginForm()
	if form.validate_on_submit():
		flash('login requested for user {}, remember me={}'.format(form.username.data,form.remember_me.data))
		return redirect(url_for('home'))
	return render_template('login.html',title='sign in',form=form)

if __name__=='__main__':
	app.run( debug=True)