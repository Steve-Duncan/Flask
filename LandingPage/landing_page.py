from flask import Flask,render_template
app = Flask(__name__)

# @app.route('/')
# def greeting():
# 	return render_template('index.html',name = 'Steve')
# app.run(debug=True)


# @app.route('/ninjas')
# def ninjas():
# 	return render_template('ninjas.html')
# app.run(debug=True)


@app.route('/dojos/new')
def dojos():
	return render_template('new_dojos.html')
app.run(debug=True)