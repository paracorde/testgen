from . import generate

import flask
import flask_wtf
import wtforms
from flask import request

import os

app = flask.Flask('gen')
app.secret_key = os.environ.get('FLASK_SECRET_KEY')

class ContentForm(flask_wtf.FlaskForm):
   content = wtforms.TextAreaField('Content to generate the quiz on', validators=[wtforms.validators.InputRequired()])
   num_mcq = wtforms.IntegerField('Number of multiple choice questions: ', validators=[wtforms.validators.InputRequired(), wtforms.validators.NumberRange(0, 5)])
   num_saq = wtforms.IntegerField('Number of short answer questions: ', validators=[wtforms.validators.InputRequired(), wtforms.validators.NumberRange(0, 5)])




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
       flask.session['content'] = form.content.data
       # quiz_data = generate.generate_quiz(form.content.data) # this doesn't generate anything
       num_mcq = form.num_mcq.data
       num_saq = form.num_saq.data
       quiz_data = generate.generate_questions(form.content.data, num_mcq, num_saq) # this generates things and runs the api!!!!
       quiz = generate.generate_quiz_form(quiz_data)
       flask.session['quiz_data'] = quiz_data
       return flask.render_template('quiz.html.jinja2', quiz_data=quiz_data, quiz=quiz)

@app.route('/gradequiz', methods=('POST',)) 
def grade_quiz():
    content = flask.session['content']
    quiz_data = flask.session['quiz_data']
    quiz = generate.generate_quiz_form(quiz_data) # for simplicity's sake, results are a colorized form with comments and grades
    if quiz.validate_on_submit():
        filled_quiz, (score, score_max), saq = generate.generate_filled_quiz_form(content, quiz_data, quiz)
        return flask.render_template('results.html.jinja2', quiz_data=quiz_data, quiz=filled_quiz, saq=saq, score=score, score_max=score_max)
    return ':('