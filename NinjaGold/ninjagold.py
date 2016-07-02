from flask import Flask, render_template, session, request, redirect,Markup
import random, datetime
app=Flask(__name__)
app.secret_key="Br@1nCl0ud"								#set secret key to encrypt the session

@app.route('/')
def index():
	session.clear()										#start with clear session
	return render_template("index.html")


@app.route('/process_money',methods=['POST'])
def process():

	if 'money' not in session:							#initialize money in session
		session['money']=0

	location=request.form['location']					#get location (which button was pressed)
	if location=='farm':								#and set the range of values for that location
		low=10
		high=21
	elif location=='cave':
		low=5
		high=11
	elif location=='house':
		low=2
		high=6
	elif location=='casino':
		low=-50
		high=51
	booty = random.randrange(low, high)					#get a random number in the range set above
	session['money'] += booty							#and add that number to a counter

	today = datetime.datetime.now().strftime('%Y/%m/%d %H:%M %p')	#get date and time
	
	#generate activity message for gold gain/lost from each location; this dynamically creates paragraphs for the process template
	#and set text color to green for gain or red for lost
	if location != 'casino':
		msg = Markup('<p class="textgreen">Earned ' + str(booty) + ' golds from the '+ location + '! (' + today + ')</p>')
		textcolor='textgreen'
	elif booty > 0:
		msg = Markup('<p class="textgreen">Entered a casino and won ' + str(booty) + ' golds...Hooray! ('+ today + ')</p>')
		textcolor='textgreen'
	else:
		msg = Markup('<p class="textred">Entered a casino and lost ' + str(abs(booty)) + ' golds...Ouch... ('+ today + ')</p>')
		textcolor='textred'
	print msg

	if 'msg' not in session:							#check if msg already exists in session
		session['msg'] = msg 						#if it does not, create msg session
	else:
		session['msg'] = session['msg'] + msg 			#if it does, add msg to session

	#render template, passing values for amount gained/lost, activity message, and text color
	return render_template('/process.html',amt=session['money'],msg=session['msg'],textcolor=textcolor)

@app.route('/reset',methods=['POST'])
def reset():
	return redirect('/')

app.run(debug=True)