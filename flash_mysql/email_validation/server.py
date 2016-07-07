from flask import Flask, render_template, request, redirect , session, url_for
from mysqlconnection import MySQLConnector
import re, datetime

#regex for valid email format
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

app=Flask(__name__)
app.secret_key="Br@1nCl0ud"
mysql = MySQLConnector(app,'email')

@app.route('/',methods=['GET'])
def index():
	return render_template('index.html')


@app.route('/process',methods=['POST'])
def submit():
	#set initial value of condition to valid
	isvalid = 'valid'
	
	email=request.form['email']
	#validate no blank fields
	if len(email)<1:
		return redirect('/')

	#validate email address
	if not EMAIL_REGEX.match(email):
		#set condition to not valid
		isvalid = 'notvalid'
		#message to return
		msg = 'Email is not valid!'
		return render_template('index.html',isvalid=isvalid,msg=msg)
	else:
		#set contidion to valid
		isvalid = 'valid'
		#SQL query to add email address to database
		query = "INSERT INTO email_addresses (email) VALUES (:email)"
		#create a dictionary of data from the POST data received.
		data = {'email': email}
		# Run query, with dictionary values injected into the query.
		mysql.query_db(query, data)
		#SQL query to return all addresses
		query = "SELECT id,email,DATE_FORMAT(create_time,'%m/%d/%Y %l:%m%p') AS 'date' FROM email_addresses;"
		data = {'email': email}
		#put all email addresses in variable
		addresses=mysql.query_db(query, data)

		return render_template('process.html',email=email,email_list=addresses)
	return redirect('/')


@app.route('/delete/<email_id>',methods=['POST'])
def delete(email_id):
	#SQL query to delete an address
	query = "DELETE FROM email_addresses WHERE id = :id"
	data = {'id': email_id}
	#run the query
	mysql.query_db(query, data)

	#query to return addresses
	query = "SELECT id,email,DATE_FORMAT(create_time,'%m/%d/%Y %l:%m%p') AS 'date' FROM email_addresses;"
	addresses=mysql.query_db(query)
	#render the process page again, make success messabe invisible, and list remaining addresses
	return render_template('process.html',email='',visible='hide',email_list=addresses)


app.run(debug=True)