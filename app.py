from flask import Flask, render_template, url_for

app = Flask(__name__)

topics = [
	{"title": "Animals"},
	{"title": "School"},
	{"title": "Traveling"},
	{"title": "Home"}
]

@app.route("/")
@app.route("/login")
def login():
	return render_template("login.html")

@app.route("/register")
def register():
	return render_template("register.html")

@app.route("/main")
def main():
	return render_template("main.html", topics=topics, length=len(topics))

if __name__ == "__main__":
	app.run(debug=True)
