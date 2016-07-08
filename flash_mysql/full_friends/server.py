from flask import Flask, render_template, request, redirect
import datetime
from mysqlconnection import MySQLConnector

app = Flask(__name__)
#create instance of sql connector, connecting to the friendsdb schema
mysql = MySQLConnector(app,'friendsdb')
############################################################
#index
@app.route('/')
def index():
	#SQL query to return all user records
	query="SELECT id, CONCAT(first_name,' ',last_name) AS 'name', email, DATE_FORMAT(created_at,'%m/%d/%Y %l:%m%p') AS 'created' FROM friends;"
	#run query and store results in variable
	friends = mysql.query_db(query) 
	#run query and open index page, passing results
	return render_template('index.html', friends=friends)
############################################################
#create
@app.route('/friends', methods=['GET','POST'])
def create():
	#check value of submit button
	if request.form['submit']=='Add User?':
		#if submit button was on the index page, open the edit form
		return render_template('edit.html')	
	else:	
		#if submit button was on edit page, create SQL query to add record
		query="INSERT INTO friends (first_name,last_name,email) VALUES (:first_name, :last_name, :email)"
		data={
				'first_name': request.form['first_name'],
				'last_name': request.form['last_name'],
				'email': request.form['email']
		}
		#run the query to add the record
		mysql.query_db(query,data)
		#return to index page
		return redirect('/')
	
############################################################
#edit
@app.route('/friends/<user_id>/edit',methods=['GET'])
def edit(user_id):
	#SQL query to return record for selected user
	query="SELECT id, first_name,last_name,email FROM friends WHERE id= :id;"
	data = {'id': user_id}
	#run the query to return the record
	friends = mysql.query_db(query,data)
	#open edit page, passing selected record
	return render_template('edit.html',friends=friends)

############################################################
#update
@app.route('/friends/<user_id>', methods=['POST'])
def update(user_id):
	#SQL query to update record
	query="UPDATE friends \
		SET first_name = :first_name, last_name = :last_name, email = :email \
		WHERE id = :id"
	data={
			'id': user_id,
			'first_name': request.form['first_name'],
			'last_name': request.form['last_name'],
			'email': request.form['email']
	}
	#run the query to update the record
	mysql.query_db(query,data)
	#return to index page
	return redirect('/')
############################################################
#destroy
@app.route('/friends/<user_id>/delete',methods=['POST'])
def destroy(user_id):
	#SQL query to delete selected user
	query = "DELETE FROM friends WHERE id= :id;"
	data = {'id': user_id}
	#run query to delete record
	friends = mysql.query_db(query,data)
	#return to index page
	return redirect('/')
############################################################

app.run(debug=True)




