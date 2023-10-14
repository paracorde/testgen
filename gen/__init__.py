import flask
app = flask.Flask('gen')

@app.route('/')
def index():
    return flask.render_template('home.html')