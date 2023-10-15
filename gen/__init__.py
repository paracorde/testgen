from . import generate

import flask
import flask_wtf
import wtforms

import os

app = flask.Flask('gen')
app.secret_key = os.environ.get('FLASK_SECRET_KEY')

class ContentForm(flask_wtf.FlaskForm):
    content = wtforms.TextAreaField('Content to generate the quiz on')

class QuizForm(flask_wtf.FlaskForm):
    mcq = []

@app.route('/', methods=('GET',)) # posts to /quiz
def index():
    form = ContentForm()
    return flask.render_template('index.html.jinja2', form=form)

@app.route('/quiz', methods=('POST',)) # posts to /gradequiz
def display_quiz():
    form = ContentForm()
    if form.validate_on_submit():
        quiz_data = generate.generate_quiz(form.content.data)
        quiz = generate.generate_quiz_form(quiz_data)
        flask.session['quiz_data'] = quiz_data
        return flask.render_template('quiz.html.jinja2', quiz_data=quiz_data, quiz=quiz)

@app.route('/gradequiz', methods=('POST',))
def grade_quiz():
    quiz_data = flask.session['quiz_data']
    flask.session.pop('quiz_data') # no idea if this pop also returns the value so it's just two separate calls
    quiz = generate.generate_quiz_form(quiz_data) # for simplicity's sake, results are a colorized form with comments and grades
    if quiz.validate_on_submit():
        filled_quiz, (score, score_max), comments = generate.generate_filled_quiz_form(quiz_data, quiz)
        return flask.render_template('results.html.jinja2', quiz_data=quiz_data, quiz=filled_quiz)
    return ':('