from flask import Flask, render_template, request, redirect, session, flash
import datetime, re
from mysqlconnection import MySQLConnector
from flask.ext.bcrypt import Bcrypt

# create a regular expression object that we can use run operations on
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

app=Flask(__name__)
app.secret_key="Br@1nCl0ud"

bcrypt=Bcrypt(app)

#create instance of sql connector, connecting to the friendsdb schema
mysql = MySQLConnector(app,'friendsdb')

############################################################
#index
@app.route('/', methods=['GET','POST'])
def index():
	
	return render_template('index.html',login='show',register='hide')

############################################################
#login
@app.route('/login',methods=['POST'])
def login():
	#get values from login form
	email=request.form['email']
	password=request.form['password']

	#check if email found in database
	query="SELECT email, password FROM friends WHERE email= :email LIMIT 1;"
	data = {
		'email': email
		}
	#run the query to return the record
	friends = mysql.query_db(query,data)
	#if email found
	if friends:
		for friend in friends:
			#check the password to compare with hashed value in database
			if bcrypt.check_password_hash(friends[0]['password'],password):
				#render success page
				return render_template('success.html', msg='Login')
				#a session of user id could be set here for use to verify user is logged in later...
			else:
				flash( "Password incorrect. Please try again." ) 
				#add error message for this
	else:
		#email not found in database, need to register
		#display message on registration page
		return render_template('index.html',login='hide',register='show')
	return redirect('/')
############################################################
#register
@app.route('/register',methods=['POST'])
def register():
	#get values from registration form
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	email = request.form['email']
	password = request.form['password']
	confirm_password = request.form['confirm_password']

	###validation###
	#check for empty fields
	for field in ['first_name','last_name']:
		if len(field)<1:
			print (field,'cannot be empty!')
			flash('{} field cannot be empty!'.format(field))
		#check if field contains at least 2 characters 
		elif len(field)<2:
			flash('{} field must contain at least 2 characters!'.format(field))

	#check for empty field
	if len(email)<1:
		flash('Email cannot be blank!')
	#check if email is valid format
	elif not EMAIL_REGEX.match(email):
		flash('Invalid email address')

	#check for empty field
	if len(password)<1:
		flash("Password field cannot be empty!")
	#check if password is at least 8 characters long
	elif len(password)<8:
		flash("Password length must be at least 8 characters!")
	#verify passwords match
	elif not confirm_password==password:
		flash("Passwords do not match!")
	else:
		###encrypt the password before inserting to database
		pw_hash=bcrypt.generate_password_hash(password)
		#query to add user to database
		query="INSERT INTO friends (first_name,last_name,email,password) VALUES (:first_name, :last_name, :email, :pw_hash)"
		data={
				'first_name': first_name,
				'last_name': last_name,
				'email': email,
				'pw_hash': pw_hash
		}
		#run the query to add the record
		mysql.query_db(query,data)
		#render success page
		return render_template('success.html',msg='Registration' )

	return redirect('/')
############################################################

app.run(debug=True)


