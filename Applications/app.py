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

@app.route('/send_mail')
def send_mail():
	return render_template('send_mail.html')

@app.route('/send_mail', methods=['POST'])
def send_mail_post():
    text = request.form['message']
    from1 = request.form['from']
    to = request.form['to']
    password = request.form['password']
    subject = request.form['subject']
    body = request.form['body']
    sendmail(from1,password,to,subject,body,text)
    result = request.form
    return render_template('mail_sent.html',result=result,value=text)

if __name__ == '__main__':
	app.run(debug=True)