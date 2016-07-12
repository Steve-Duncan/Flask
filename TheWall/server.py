from flask import Flask, render_template, request, redirect, Markup, session, url_for
import datetime, re
from mysqlconnection import MySQLConnector
from flask.ext.bcrypt import Bcrypt

# create a regular expression object that we can use run operations on
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')


app=Flask(__name__)
app.secret_key="Br@1nCl0ud"

bcrypt=Bcrypt(app)
#create instance of sql connector, connecting to the friendsdb schema
mysql = MySQLConnector(app,'wall')

############################################################
#this function gets all messages from database
def get_messages():
	query="SELECT CONCAT(users.first_name,' ',users.last_name) AS 'name', DATE_FORMAT(messages.create_time, '%M %D, %Y') AS 'create_date', message \
	FROM MESSAGES JOIN users ON messages.user_id=users.id ORDER BY messages.create_time DESC;"
	return mysql.query_db(query)
############################################################
#index
@app.route('/')
def index():
	#set initial greeting
	greeting ='Welcome!'
	#set value of log in/log out anchor
	login='log in'
	#set value of register anchor
	register='register'
	#hide login form
	show_login='hide'
	#hide register form
	show_register='hide'
	#disable message input field and button
	enabled='disabled'
	#set default message for message input field
	new_msg_default='You must be logged in to post messages.'
	return render_template('index.html',greeting=greeting,login=login,register=register,show_login=show_login,show_register=show_register,enabled=enabled,new_msg_default=new_msg_default)

############################################################
#show login or register
@app.route('/showform/<action>', methods=['GET','POST'])
def showform(action):
	#hide the message input field
	show_msg_input='hide' 
	#set values of login/logout and register anchors to blank
	login=''
	register='' 
	#if login link selected, show login form and hide register form
	if action=='login':
		show_login='show'
		show_register='hide'
	else:
		#show register form and hide login form
		show_login='hide'
		show_register='show'

	return render_template('index.html',login=login,register=register,show_login=show_login,show_register=show_register,show_msg_input=show_msg_input)


############################################################
#log off
@app.route('/logoff')
def logoff():
	#go back to initial index page at logoff
	return redirect('/')

############################################################
#login
@app.route('/login',methods=['GET', 'POST'])
def login():
	#get values from login form
	email=request.form['email']
	password=request.form['password']

	#check if email found in database
	query="SELECT id,first_name,CONCAT(first_name,' ',last_name) AS 'name',email, password FROM users WHERE email= :email LIMIT 1;"
	data = {
		'email': email
		}
	#run the query to return the record
	users = mysql.query_db(query,data)
	#if email found
	if users:
		for user in users:
			#check the password to compare with hashed value in database
			if bcrypt.check_password_hash(users[0]['password'],password):
				#login was successful
				#sett greeting to user's name
				greeting='Welcome, ' + users[0]['first_name'] + '!'
				#hide the login and register forms
				show_login='hide'
				show_register='hide'
				#change login anchor to log out
				login='log out'
				#set register anchor to blank
				register=''
				#set session variables for user name, id, and greeting 
				session['user']=users[0]['name']
				session['user_id']=users[0]['id']
				session['greeting']=greeting
				#enable the message input field and button
				enabled = 'enabled'
				#unhide the message input field
				show_msg_input='show'
				#unhide div that displays messages
				show_messages='show'
				#call function to get all messages
				all_messages=get_messages();
				
				return render_template('index.html',show_login=show_login,show_register=show_register,show_messages=show_messages,all_messages=all_messages,greeting=greeting,login=login,register=register,enabled=enabled,show_msg_input=show_msg_input)

			else:
				flash( "Password incorrect. Please try again." ) 
				
	else:
		#email not found in database, need to register
		##need to add error message to form
		##need to add link to return to index if not registering
		return redirect('/showform/register')
	return redirect('/')
############################################################
#register
@app.route('/register',methods=['GET','POST'])
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
		query="INSERT INTO users (first_name,last_name,email,password) VALUES (:first_name, :last_name, :email, :pw_hash)"
		data={
				'first_name': first_name,
				'last_name': last_name,
				'email': email,
				'pw_hash': pw_hash
		}
		#run the query to add the record
		mysql.query_db(query,data)
		
		#requery database to get user id
		query="SELECT id,first_name,CONCAT(first_name,' ',last_name) AS 'name',email, password FROM users WHERE email= :email LIMIT 1;"
		data = {
			'email': email
		}
		#run the query to return the record
		users = mysql.query_db(query,data)
		#set user greeting
		greeting='Welcome, ' + users[0]['first_name'] + '!'
		#set session variables for user name, id, and greeting
		session['user']=users[0]['name']
		session['user_id']=users[0]['id']
		session['greeting']=greeting
		#hide login and register forms
		show_login='hide'
		show_register='hide'
		#change login anchor to log out
		login='log out'
		#enable the message input field and button
		enabled = 'enabled'
		#unhide div that displays messages
		show_messages='show'
		#unhide the message input field
		show_msg_input='show'
		#call function to get all messages
		all_messages=get_messages();

		return render_template('index.html', show_messages=show_messages,all_messages=all_messages,greeting=greeting, login=login, register=register, enabled=enabled, show_login=show_login, show_register=show_register, show_msg_input=show_msg_input)
############################################################
@app.route('/post_msg',methods=['POST'])
def post_msg():
	
	#get new message from form
	new_msg=request.form['new_msg']
	#get user id from session
	user_id=session['user_id']
	#add message and user id to database
	query="INSERT INTO messages (user_id, message) VALUES (:user_id, :message)"
	data={
		'user_id': user_id,
		'message': new_msg
	}
	#run the query to add the record
	mysql.query_db(query,data)

	#get user name from session
	user=session['user']
	#set user greeting
	greeting=session['greeting']

	#hide login and register forms
	show_login='hide'
	show_register='hide'
	#set login anchor to log out
	login='log out'
	#enable message input field and button
	enabled = 'enabled'
	#unhide message input field
	show_msg_input='show'
	#unhide div that contains messages
	show_messages='show'
	#call function to get all messages
	all_messages=get_messages();

	return render_template('index.html', show_messages=show_messages,all_messages=all_messages,greeting=greeting, login=login, register=register, enabled=enabled, show_login=show_login, show_register=show_register, show_msg_input=show_msg_input)


############################################################
app.run(debug=True)

