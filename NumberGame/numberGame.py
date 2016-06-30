from flask import Flask,render_template,session,request,redirect
import random
app = Flask(__name__)
app.secret_key="Br@1nCl0ud"								#set secret key to encrypt the session

@app.route('/',)
def game():
 	if 'number' not in session:							#check if session already exists
  		session['number']=random.randrange(0, 100)		#set session to random number; try to guess this
  	
	return render_template("index.html")


@app.route('/guess', methods=['POST'])
def play():

	if request.form['guess']=='repeat':					#check if the play again button was pressed		
		return redirect('/')							#if so, redirect to start page

	number=session['number']							#get the target number
	guess = request.form['guess']						#get the guessed number							

	if not guess:										#if no number entered on submit, redirect to start page
		return redirect('/')									#needs better error handling here

  	if int(guess) < int(number):						#compare guess to target number and return to correct page
  		result = 'Too low!'
  		retPage = 'notIt.html'

  	elif int(guess) > int(number):
  		result = 'Too high!'
  		retPage = 'notIt.html'

  	else:
  		result = str(number)+" was the number!"
  		retPage = 'gotIt.html'
 		
  		guess=None										#clear the variable
 	return render_template(retPage, msg=result)


@app.route('/repeat',methods=['POST'])				#if the play again button was pressed
def repeat():
	session.clear()									#clear the target number from the session
	return redirect('/')							#and return to the start page

app.run(debug='True')