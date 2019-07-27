from flask import Flask, render_template, url_for, redirect, flash, request
from forms import signinForm, signupForm
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SECRET_KEY'] = '5aa6face94d8ddee195ead1c27068eec'

@app.route("/")
@app.route("/signin", methods=["GET", "POST"])
def login():
	form = signinForm()
	if form.validate_on_submit():
		"""
			QUERY LOGIN INFOR AGAINST DB AND AUTHENTICATE USER
		"""
		user = User.query.filter_by(username=form.username.data).first()

		"""
			HANDLE LOGIN USE CASES
		"""
		if user is None:
			flash("User Not Found -- Please Sign Up")
		elif user.check_password(form.password.data):
			flash("Welcome Back " + form.firstName.data + " !")
		else:
			flash("Invalid Login Credentials!")

		return redirect(url_for("main"))
	return render_template("signin.html", form=form)

@app.route("/signup", methods=["GET", "POST"])
def register():
	form = signupForm()
	if form.validate_on_submit():
		"""
			INSTANTIATE NEW USER
			HASH USER PASSWORD
			INSERT AND COMMIT USER RECORD TO DATABASE
		"""
		new_user = User(firstName=form.firstName.data, lastName=form.lastName.data, username=form.username.data)
		new_user.set_password(form.password.data)
		db.session.add(new_user)
		db.session.commit()
		db.session.close()

		"""
			ALERT USER OF PROPER REGISTRATION
		"""

		flash("Account Created! Let's Begin Studying!", "success")
		return redirect(url_for("main"))
	return render_template("signup.html", form=form)

@app.route("/main")
def main():
	return render_template("main.html")


"""
	DATABASE
"""
def init_db():
	global db
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
	app.config['SECRET_KEY'] = '5aa6face94d8ddee195ead1c27068eec'
	app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
	db = SQLAlchemy(app)

init_db()

"""
	USER MODEL
"""
class User(db.Model):
	__tablename__ = 'users'
	__table_args__= {'extend_existing': True}

	id = db.Column(db.Integer, primary_key=True)
	firstName = db.Column(db.String(80))
	lastName = db.Column(db.String(80))
	username = db.Column(db.String(20))
	password_hash = db.Column(db.String(128))

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

"""
	TOPIC MODEL
"""

class Topic(db.Model):
	__tablename__ = 'topics'
	__table_args__ = {'extend_existing': True}

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(128))

	def __init__(self, title):
		self.title = title

"""
	FLASHCARD MODEL
"""

class Card(db.Model):
	__tablename__ = 'cards'
	__table_args__ = {'extend_existing': True}

	id = db.Column(db.Integer, primary_key=True)
	front = db.Column(db.String(128)) #STORES FRONT OF FLASHCARD
	back = db.Column(db.String(128)) #STORES BACK OF flashcard

	def __init__(self, front, back):
		self.front = front
		self.back = back

db.create_all()
db.session.commit()

if __name__ == "__main__":
	app.run(debug=True)
