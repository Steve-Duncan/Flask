from flask import Flask,render_template
app = Flask(__name__)

#part 1
# @app.route('/')
# def greeting():
# 	return render_template('index.html',name = 'Steve')
# app.run(debug=True)

#part 2
# @app.route('/ninjas')
# def ninjas():
# 	return render_template('ninjas.html')
# app.run(debug=True)

#part 3
@app.route('/dojos/new')
def dojos():
	return render_template('new_dojos.html')
app.run(debug=True)