from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
app.secret_key="teenage"

@app.route('/')
def index():
	return render_template('/index.html')

@app.route('/ninja/')
#this handles url of /ninja or /ninja/
def noninja():
	# create variable with file name of image
	turtle='images/TMNT.jpg'
	# pass the filename back to template
 	return render_template('/ninja.html',turtle=turtle)

@app.route('/ninja/<vararg>/')
def ninja(vararg):
	# gets argument from URL; assigns image file to arguments passed
	if vararg=='blue':
		turtle='images/leonardo.jpg'
	elif vararg=='orange':
		turtle='images/michelangelo.jpg'
	elif vararg=='red':
		turtle='images/raphael.jpg'
	elif vararg=='purple':
		turtle='images/donatello.jpg'
	else:
		turtle='images/notapril.jpg'
	# pass image file name back to template
	return render_template('/ninja.html',turtle=turtle)


app.run(debug=True)