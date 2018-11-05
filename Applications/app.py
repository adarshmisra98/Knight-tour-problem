from flask import Flask, render_template, request
from encode import *
from decode import *

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/encode')
def encode():
	return render_template('encode.html')

@app.route('/decode')
def decode():
	return render_template('decode.html')

@app.route('/decode', methods=['POST'])
def my_post():
	file = request.form['files']
	ans = decoder(file)
	return render_template('message.html',value=ans)

@app.route('/encode', methods=['POST'])
def my_form_post():
    text = request.form['text']
    text = create_file(text)
    result = request.form
    return render_template('ready.html',result=result,value=text)

if __name__ == '__main__':
	app.run(debug=True)