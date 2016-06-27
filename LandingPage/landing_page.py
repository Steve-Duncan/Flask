from flask import Flask,render_template
app = Flask(__name__)

@app.route('/')

def greeting():
	return render_template('index.html',name = 'Steve')

app.run(debug=True)