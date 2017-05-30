from flask import render_template, redirect, flash, request, Flask, session, send_file
from forms import *
from queries import *
from imageLib import *

import sqlite3, time, json

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'secret_key'



@app.route("/")
@app.route("/index")
def index():
	return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
	loginForm = login_form()
	username = loginForm.data['username']
	password = loginForm.data['password']
	if (loginForm.validate_on_submit()):
		session['username'] = username
		session['logged_in'] = True

		return render_template('index.html')
	else:
		return render_template('login.html', title='Sign In', form= loginForm)

@app.route("/logout")
def logout():
	session['logged_in'] = False
	return render_template("index.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	signupForm = signup_form()
	if(signupForm.validate_on_submit()):
		session['username'] = signupForm.data["username"]
		session['logged_in'] = True
		insertUser(signupForm.data)

		return render_template('index.html')
	else:
		return render_template('signUp.html', title='signUp', form = signupForm)


@app.route("/makeProxies")
def makeProxies():
	cards = getAllCards()
	cards = sorted(cards, key = lambda x: x[0])

	return render_template("proxies.html", allCards = cards)

@app.route('/addCard', methods=['POST'])
def addCard():
	api_card_id = request.form['card_id']
	user = session["username"]

	insertUserProxyCard(user, api_card_id)
	return "Received!"

@app.route('/removeCard', methods=['POST'])
def removeCard():
	api_card_id = request.form['card_id']
	user = session["username"]

	removeUserProxyCard(user, api_card_id)
	return "Received!"

@app.route('/createImage', methods=['GET', 'POST'])
def createImage():
	user = session["username"]

	cards = getUserProxyCards(user)
	cardImageFiles = ["static/images/cardImages/" + card[3] + ".png" for card in cards]

	fillProxies(cardImageFiles)
	return send_file('proxies.pdf',
					 mimetype='text/pdf',
					 attachment_filename='proxies.pdf',
					 as_attachment=True)


@app.route("/myProxies")
def myProxies():
	user = session["username"]
	cards = getUserProxyCards(user)
	print(cards)
	return render_template("userProxies.html", allCards = cards)


@app.route("/deleteAllUserProxies")
def deleteAllUserProxies():
	user = session["username"]
	cards = removeUserProxyCards(user)
	return render_template("userProxies.html", allCards = cards)


if(__name__ == "__main__"):
	app.run(debug = True)

