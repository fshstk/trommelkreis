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
    return render_template('upload.jinja')

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
    pages = (
        {
        'title': '<i class="fa fa-home"></i>',
        'url': '/',
        'class': 'text-dark'
        },
        {
        'title': 'Info',
        'url': '/info',
        'class': 'text-dark'
        },
        {
        'title': 'Archiv',
        'url': '/archiv',
        'class': 'text-dark'
        },
        {
        'title': 'Mitmachen',
        'url': '/upload',
        'class': 'text-primary'         # highlight color
        },
        {
        'title': '<i class="fa fa-envelope-o"></i>',
        'url': 'subscribe',
        'class': 'text-dark ml-auto'    # move right
        }
    )
    return dict(pages = pages)

################################################################################

if __name__ == '__main__':
    app.run(debug = True)
