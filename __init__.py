from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/challenge')
def challenge():
    return render_template('challenge.html')

@app.route('/archiv')
def archiv():
    return render_template('archiv.html')

@app.route('/session')
def session():
    return render_template('session.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug = True)