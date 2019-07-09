from flask import Flask, render_template, url_for, redirect, flash
from forms import registrationForm, loginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '5aa6face94d8ddee195ead1c27068eec'

topics = [
	{"title": "Animals"},
	{"title": "School"},
	{"title": "Traveling"},
	{"title": "Home"},
	{"title": "Personal"}
]

@app.route("/")
@app.route("/login")
def login():
	form = loginForm()
	if form.validate_on_submit():
		if form.email.data == "admin@blog.com" and form.password.data == "password":
			flash('You Have Been Logged In')
			return redirect(url_for('main'))
		else:
			flash('Login Unsuccessful. Please Check Username and Password!')
	return render_template("login.html", form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
	form = registrationForm()
	if form.validate_on_submit():
		flash('Account Created', 'success')
		return redirect(url_for('login'))
	return render_template("register.html", form=form)

@app.route("/main")
def main():
	return render_template("main.html", topics=topics, length=len(topics))

if __name__ == "__main__":
	app.run(debug=True)
