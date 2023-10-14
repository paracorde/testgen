import os

import flask
import flask_wtf
import wtforms

app = flask.Flask('gen')
app.secret_key = os.environ.get('FLASK_SECRET_KEY')

class ContentForm(flask_wtf.FlaskForm):
    content = wtforms.TextAreaField('Content to generate the quiz on')

@app.route('/', methods=('GET', 'POST'))
def index():
    form = ContentForm()
    if flask.request.method == 'POST':
        print('hiii', form.validate_on_submit(), form.errors)
        if form.validate_on_submit():
            print(form.content)
            return flask.render_template('quiz.html.jinja2', quiz='this should show you a quiz based on this content but just returning the text for now to show its been read' + form.content.data)
    return flask.render_template('index.html.jinja2', form=form)
