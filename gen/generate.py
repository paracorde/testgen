import openai
import flask_wtf
import wtforms

import random

delimiter = ' XWX '

prompt = f'''
Create a multiple choice question with 4 choices and the index of the correct choice at the end, with the indexes starting at 0. Ensure your response is always formatted like this: 'question{delimiter}option1{delimiter}option2{delimiter}option3{delimiter}option4{delimiter}correctindex'. For example, with a paragraph about math, your response must look like this: '2+2={delimiter}2{delimiter}3{delimiter}4{delimiter}5{delimiter}2'.
'''

def generate_questions(content):
    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages = [
            {'role': 'system', 'content': content},
            {'role': 'system', 'content': prompt}
        ]
    )
    
    cont = response.choices[0].message.content.split(delimiter)
    print(cont)
    # cont = 'In which city did Vincent van Gogh spend the last years of his life and create some of his most renowned artworks?$@~Paris$@~Amsterdam$@~Arles$@~Madrid$@~3'.split(delimiter)
    # q = {}

    # q['question'] = cont[0]
    # q['options'] = cont[1:-1]
    # q['answer'] = int(cont[-1])

    # assert(q['answer'] <= len(q['options']))

    # return q

def generate_quiz(content):
    qs = []
    for i in range(2):
        qs.append({'question': f'Question {i+1}', 'options': ['A', 'B', 'C', 'D'], 'answer': 1})
    return {'mcq': qs, 'saq': ['this is a short answer', 'this is another short answer']}

def generate_quiz_form(questions):
    class QuizForm(flask_wtf.FlaskForm):
        pass
    
    for i, v in enumerate(questions['mcq']):
        setattr(QuizForm, f'mcq{i}', wtforms.RadioField(v['question'], choices=v['options'], validators=[wtforms.validators.InputRequired()]))
    
    for i, v in enumerate(questions['saq']):
        setattr(QuizForm, f'saq{i}', wtforms.TextAreaField(v, validators=[wtforms.validators.InputRequired()]))
    
    return QuizForm()

def generate_filled_quiz_form(questions, quiz): # grades quiz, returns filled quiz form with some details
    class QuizForm(flask_wtf.FlaskForm):
        pass
    
    for i, v in enumerate(questions['mcq']):
        attr = f'mcq{i}'
        setattr(QuizForm, attr, wtforms.RadioField(v['question'], choices=v['options'], default=getattr(quiz, attr).data, render_kw={'disabled': 'disabled'}))
    
    for i, v in enumerate(questions['saq']):
        attr = f'saq{i}'
        setattr(QuizForm, attr, wtforms.TextAreaField(v, default=getattr(quiz, attr), render_kw={'disabled': 'disabled'}))
    
    score = score_max = 10
    comments = ''
    return QuizForm(), (score, score_max), comments
        