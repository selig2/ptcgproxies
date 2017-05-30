from flask_wtf import Form
from wtforms import StringField, PasswordField, RadioField, IntegerField, SelectField, BooleanField
from wtforms.validators import DataRequired, ValidationError
import sqlite3
from flask import session

class login_form(Form):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	# source: http://flask.pocoo.org/snippets/64/
	def validate(self):
		if(not Form.validate(self)):
			return False

		username = self.username.data
		password = self.password.data
		conn = sqlite3.connect('pokemontcg.db')
		cur = conn.cursor()
		query = 'SELECT password FROM User WHERE username = ?'
		cur.execute(query, (username,))
		result = cur.fetchone()
		conn.close()

		if(result == None):
			self.username.errors.append('Invalid Username')
			return False
		elif(result != None and result[0] != password):
			self.password.errors.append('Invalid Password')
			return False

		return True



class signup_form(Form):
	email = StringField('Email', validators=[DataRequired()])
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	rePassword = PasswordField('rePassword', validators=[DataRequired()])
	# source: http://flask.pocoo.org/snippets/64/
	def validate(self):
		if(not Form.validate(self)):
			return False

		username = self.username.data
		password = self.password.data
		rePassword = self.rePassword.data

		conn = sqlite3.connect('pokemontcg.db')
		cur = conn.cursor()
		query = 'SELECT password FROM User WHERE username = ?'
		cur.execute(query, (username,))
		result = cur.fetchone()
		conn.close()
		
		if(result != None):
			self.username.errors.append("Invalid username")
			return False
		if(password != rePassword):
			self.rePassword.errors.append("Passwords don't match.")
			return False
		return True






