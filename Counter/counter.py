from flask import Flask,render_template,session,request,redirect
app = Flask(__name__)
app.secret_key="Br@1nCl0ud"						#set secret key to encrypt the session

@app.route('/')
def counter():
	#session.clear()							#use this to clear the session
	if 'count' in session:						#check if session already exists

	  	tmpcount=session['count']				#set tmp variable for count
	  	tmpcount = int(tmpcount) + 1 			#convert tmp count to integer and increment by 1
	  	session['count'] = str(tmpcount)		#convert tmp count to str and set as session

	else:

	  	session['count'] = '1'					#set session as string

	return render_template("index.html")


@app.route('/ninja', methods=['POST'])
def plustwo():
	action=request.form['action']				#get the value of the submit button pressed (ninja or reset)
	if (action=='reset'):
		session.clear()							#this will clear the session, and be reset to 1 when redirected back to '/'
	else:										#this will increment count by 1, and by another when redirected back to '/'
	  	tmpcount=session['count']				#set tmp variable for count
	  	tmpcount = int(tmpcount) + 1 			#convert tmp count to integer and increment by 1
	  	session['count'] = str(tmpcount)		#convert tmp count to str and set as session

	return redirect('/')

app.run(debug='True')