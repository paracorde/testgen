import openai
import flask_wtf
import wtforms

import random

delimiter = '--@'

instructions = f'''Given the information above, you have two tasks. Task 1: If the tag [MCQ] is seen, create a multiple choice question with 4 choices and the index of the correct choice at the end. Ensure your response is always formatted like this: 'question{delimiter}option1{delimiter}option2{delimiter}option3{delimiter}option4{delimiter}correctIndex'. For example, with a paragraph about math, your response must look like this: '2+2={delimiter}2{delimiter}3{delimiter}4{delimiter}5{delimiter}2'. The output must be a single line omitting option letters and strictly without additional context. If the tag [SAQ] is seen, generate a single short answer question on one line strictly without context.'''
def generate_questions(content, num_mcq, num_saq):
    questions = {'mcq': [], 'saq': []}
    chatlog = [
        {'role': 'system', 'content': content},
        {'role': 'system', 'content': instructions}
    ]
    i = 0
    while i < num_mcq + num_saq:
        if i < num_mcq: # still generating mcqs
            prompt = '[MCQ]'
        else: # generating saqs
            prompt = '[SAQ]'
        chatlog.append({'role': 'user', 'content': prompt})
        response = openai.ChatCompletion.create(
            model = 'gpt-3.5-turbo',
            messages = chatlog
        )

        cont = response.choices[0].message.content
        if i < num_mcq: # interpret message as mcq
            scont = cont.split(delimiter)
            try:
                q = {'question': scont[0], 'options': scont[1:-1], 'answer': int(scont[-1])}
                assert q['answer'] <= len(q['options']) # ensure that the "correct" answer actually points to some value
            except:
                i += 1
                continue # try again :(
            questions['mcq'].append(q)
        else:
            questions['saq'].append(cont)
        i += 1
        chatlog.append({'role': 'assistant', 'content': cont})
    return questions

def generate_quiz(content): # just for testing
    # qs = []
    # for i in range(2):
    #     qs.append({'question': f'Question {i+1}', 'options': ['A', 'B', 'C', 'D'], 'answer': 1})
    # return {'mcq': qs, 'saq': ['this is a short answer', 'this is another short answer']}
    return {'mcq': [{'question': "What is the title of Isidore's best known work on the overland trade route from Antioch to India?", 'options': ['The Parthian Trade', 'The Silk Road', 'A Journey around Parthia', 'The Caravan Route'], 'answer': 3}, {'question': 'When did Isidore write "The Parthian Stations"?', 'options': ['1st century BC', '2nd century BC', '1st century AD', '2nd century AD'], 'answer': 3}], 'saq': ['What is the debated value of Isidore\'s distances in the "The Parthian Stations"?', 'Wow!']}

def generate_quiz_form(questions):
    class QuizForm(flask_wtf.FlaskForm):
        pass
    
    for i, v in enumerate(questions['mcq']):
        setattr(QuizForm, f'mcq{i}', wtforms.RadioField(v['question'], choices=v['options'], validators=[wtforms.validators.InputRequired()]))
    
    for i, v in enumerate(questions['saq']):
        setattr(QuizForm, f'saq{i}', wtforms.TextAreaField(v, validators=[wtforms.validators.InputRequired()]))
    
    return QuizForm()

def generate_filled_quiz_form(content, questions, quiz): # grades quiz, returns filled quiz form with some details
    class QuizForm(flask_wtf.FlaskForm):
        pass
    
    score = 0
    for i, v in enumerate(questions['mcq']):
        attr = f'mcq{i}'
        answer = getattr(quiz, attr).data
        if answer == v['options'][v['answer']]:
            score += 1
        setattr(QuizForm, attr, wtforms.RadioField(v['question'], choices=v['options'], default=getattr(quiz, attr).data, render_kw={'disabled': 'disabled'}))
    
    answers = []
    for i, v in enumerate(questions['saq']):
        attr = f'saq{i}'
        answer = getattr(quiz, attr).data
        answers.append(answer)
        setattr(QuizForm, attr, wtforms.TextAreaField(v, default=answers, render_kw={'disabled': 'disabled'}))
    
    score_max = len(questions['mcq']) + len(questions['saq'])*10
    saq = grade_saqs(content, questions, answers)
    # saq = [(7, 'Your response accurately identifies "The Parthian Stations" as Isidore\'s best known work and mentions that it describes the trade routes maintained by the Arsacid Empire. However, it could be improved by providing more specific details about the content of the work or its historical significance.'), (3, 'Thing')] # can be used for testing
    
    for s in saq:
        score += s[0]
    
    return QuizForm(), (score, score_max), saq

grading_instructions = f'''Based on your knowledge and the short answer prompt given, grade the response given on a scale from 0-10. Include an explanation of the grade that directly addresses the student in second-person. Ensure that your response is in the format "score{delimiter}explanation" with strictly no additional context. For example, a proper response would be "8{delimiter}Your response is well-done, but has a minor factual error."'''

def grade_saqs(content, questions, answers): # returns a list of tuples (score, comment)
    saq = []
    chatlog = [
        {'role': 'system', 'content': content},
        {'role': 'system', 'content': grading_instructions}
    ]
    i = 0
    while i < len(questions['saq']):
        prompt = f'''Prompt: {questions['saq'][i]}\nStudent response: {answers[i]}'''
        chatlog.append({'role': 'user', 'content': prompt})
        response = openai.ChatCompletion.create(
            model = 'gpt-3.5-turbo',
            messages = chatlog
        )
        i += 1
        cont = response.choices[0].message.content
        try:
            conts = cont.split(delimiter)
            saq.append((int(conts[0]), conts[1]))
            assert conts[0] in range(11)
        except:
            continue
        # i += 1
        chatlog.append({'role': 'assistant', 'content': cont})
    return saq
