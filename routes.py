from flask import Flask, render_template, url_for, redirect, flash
from forms import signinForm, signupForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '5aa6face94d8ddee195ead1c27068eec'

@app.route("/")
@app.route("/signin", methods=["GET", "POST"])
def login():
	form = signinForm()
	if form.validate_on_submit():
		flash("Welcome Back User!", "success")
		return redirect(url_for("main"))
	return render_template("signin.html", form=form)

@app.route("/signup", methods=["GET", "POST"])
def register():
	form = signupForm()
	if form.validate_on_submit():
		flash("Account Created! Let's Begin Studying!", "success")
		return redirect(url_for("main"))
	return render_template("signup.html", form=form)

@app.route("/main")
def main():
	return render_template("main.html")

if __name__ == "__main__":
	app.run(debug=True)
