from flask import Flask, render_template, request, redirect, session,url_for
from sqlite3 import *
from flask_mail import Mail,Message
from random import randrange
import pickle

app = Flask(__name__)
app.secret_key= "amaanshaikh"

app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = "your_email"
app.config['MAIL_PASSWORD'] = "your_password"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.route("/")
def home():
	if "username" in session:
		return render_template("home.html",name=session["username"])
	else:
		return redirect( url_for('login') )

@app.route("/login",methods=["GET","POST"])
def login():
	if request.method == "POST":
		un = request.form["un"]
		pw = request.form["pw"]
		con = None
		try:
			con = connect("calorie.db")
			cursor = con.cursor()
			sql = "select * from user where username = '%s' and password='%s'"
			cursor.execute(sql % (un,pw))
			data = cursor.fetchall()
			if len(data) == 0:
				return render_template("login.html",msg="Invalid Credentials")
			else:
				session['username'] = un
				return redirect( url_for('home') )
		except Exception as e:
			msg = "issue " + str(e)
			return render_template("login.html",msg=msg)
	else:
		return render_template("login.html")

@app.route("/resetpassword",methods=["GET","POST"])
def resetpassword():
	if request.method == "POST":
		un = request.form["un"]
		em = request.form["em"]
		con = None
		try:
			con = connect("calorie.db")
			cursor = con.cursor()
			sql = "select * from user where username = '%s' and email='%s'"
			cursor.execute(sql % (un,em))
			data = cursor.fetchall()
			if len(data) == 0:
				return render_template("login.html",msg="User Does Not Exists")
			else:
				con = connect("calorie.db")
				cursor = con.cursor()
				text = "1234567890abcdefghijklmnopqrstuvwxyz"
				pw = ""
				for i in range(6):
					pw = pw + text[randrange(len(text))]
			
				sql = "update user set password='%s' where username='%s'"
				con.execute(sql % (pw,un))
				con.commit()
				msg = Message("Welcome to Calories Burnt Predictor ",sender="your_email",recipients=[em])
				msg.body="Your password has been reset Successfully. Your new  password is " + pw
				mail.send(msg)
				return redirect( url_for('login'))
		except Exception as e:
			if con is not None:
				con.rollback()
			return render_template("signup.html",msg=str(e))
	else:
		return render_template("resetpassword.html")

@app.route("/signup",methods=["GET","POST"])
def signup():
	if request.method == "POST":
		un = request.form["un"]
		em = request.form["em"]
		con = None
		try:
			con = connect("calorie.db")
			cursor = con.cursor()
			text = "1234567890abcdefghijklmnopqrstuvwxyz"
			pw = ""
			for i in range(6):
				pw = pw + text[randrange(len(text))]
			
			sql = "insert into user values('%s','%s','%s')"
			con.execute(sql % (un,em,pw))
			con.commit()
			msg = Message("Welcome to Calories Burnt Predictor ",sender="your_email",recipients=[em])
			msg.body="Congrats u have been Registered. Your password is " + pw
			mail.send(msg)
			return redirect( url_for('login'))
		except Exception as e:
			if con is not None:
				con.rollback()
			return render_template("signup.html",msg=str(e))
	else:
		return render_template("signup.html")

@app.route("/logout",methods=["POST"])
def logout():
	session.clear()
	return redirect( url_for('login'))

@app.route("/calorie",methods=["GET","POST"])
def calorie():
	if request.method == "POST":
		age = request.form["age"]
		height = request.form["height"]
		weight = request.form["weight"]
		dur = request.form["duration"]
		hr = request.form["hr"]
		temp = request.form["temp"]
		g = request.form["r1"]
		d = [[age,height,weight,dur,hr,temp,g]]
		with open("calorie.model","rb") as f:
			model = pickle.load(f)
		res = model.predict(d)
		msg = str(res[0]) + ' calories'
		return render_template("calorie.html",msg=msg)
	else:
		return render_template("calorie.html")
		

if __name__ == "__main__":
	app.run(host="localhost",port=8000,debug=True)

			
			
