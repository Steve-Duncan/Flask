from flask import Flask, render_template, request, redirect
import datetime, re
from mysqlconnection import MySQLConnector
from flask.ext.bcrypt import Bcrypt

# create a regular expression object that we can use run operations on
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')


app=Flask(__name__)
app.secret_key="Br@1nCl0ud"

bcrypt=Bcrypt(app)
#create instance of sql connector, connecting to the friendsdb schema
mysql = MySQLConnector(app,'db')
############################################################
#index
@app.route('/')
def index():
	greeting ='Welcome.'
	log='log in'
	enabled = 'disabled'
	msg = 'You must be logged in to post or read messages.'
	visibility='hide'

	return render_template('index.html',msg=msg,visibility=visibility,log=log,enabled=enabled)
############################################################

@app.route('/login', methods=['GET'])
def login():
	return render_template('login.html')


	

@app.route('/message',methods=['POST'])
def post_msg():
	msg=request.form['message']
	print msg
	return redirect('/')

app.run(debug=True)

