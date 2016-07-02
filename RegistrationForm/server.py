from flask import Flask, render_template, request, redirect, session, flash
import re

#regex for valid email format
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

app = Flask(__name__)
app.secret_key = 'N0w!sTh3T1m3'

@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')

@app.route('/process', methods=['POST'])
def submit():
	
	#validate no blank fields
	fields = ('email', 'first_name','last_name','password','confirm_password')
	for field in fields:
		if len(request.form[field])<1:
			flash(field + ' cannot be blank')
			return redirect('/')
	
	#validate email address
	if not EMAIL_REGEX.match(request.form['email']):
		flash('Invalid email address')
		return redirect('/')
	
	#validate password is correct length and that passwords match
	if len(request.form['password']) < 9:
		flash('Password must be more than 8 characters.')
		return redirect('/')
	if request.form['confirm_password']!=request.form['password']:
		flash('Passwords do not match.')
		return redirect('/')

	flash('Thanks for submitting your information.')
	return redirect('/')

app.run(debug=True)


