from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.jinja')

@app.route('/info')
def info():
    return render_template('info.jinja')

@app.route('/challenge')
def challenge():
    return render_template('challenge.jinja')

@app.route('/archiv')
@app.route('/archive')
def archive():
    return render_template('archive.jinja')

@app.route('/session')
def session():
    return render_template('session.jinja')

@app.route('/upload')
def upload():
    return render_template('upload.jinja')

if __name__ == '__main__':
    app.run(debug = True)