from flask import Flask, render_template, request, redirect, flash
app = Flask(__name__)
app.secret_key="Br@1nCl0ud"						#set secret key to encrypt the session


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/process', methods=['GET','POST'])
def process():
	if len(request.form['name'])<1:
		flash('Name field cannot be empty. Please enter name and try again.')
		return redirect('/')	
	else:
		name = request.form['name']


	location = request.form['location']
	language = request.form['language']

	if len(request.form['comment'])<1:
		flash('Comment field cannot be empty. We really want to hear from you, so please enter comments and try again.')
		return redirect('/')
	elif len(request.form['comment'])>120:
		flash("But we don't want to hear that much from you. Please shorten your comments to fewer than 120 characters and try again.")
		return redirect('/')
	else:
		comment = request.form['comment']

	return render_template('process.html', name=name, location=location, language=language,comment=comment)

app.run(debug=True)

