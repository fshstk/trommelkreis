from flask import Flask, render_template, request, abort

app = Flask(__name__)

################################################################################

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.jinja')

@app.route('/info')
def info():
    return render_template('info.jinja')

@app.route('/archiv')
@app.route('/archiv/')
def archive():
    return render_template('archive.jinja')

@app.route('/upload')
def upload():
    return render_template('upload.jinja')

@app.route('/abo')
def subscribe():
    return render_template('subscribe.jinja')

@app.route('/challenge')
def challenge():
    return render_template('challenge.jinja')

@app.route('/archiv/<int:session>')
def session(session):
    if session is not 42:
        abort(404)
    return render_template('session.jinja', session = session)

@app.errorhandler(404) # possibly add more errors (403, 500)
def error(error):
    return render_template('error.jinja')

################################################################################

@app.context_processor
def global_vars():
    return {}

################################################################################

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True)
