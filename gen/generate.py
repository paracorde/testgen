import os

import openai

content = '''Alcott was associated with the Nonresistance Society, a radical offshoot of the abolitionist movement who believed in the systematic oppression of all human institutions opposed to divine law and the duty to withdraw immediately leaving them to collapse under the burden of their own evil.'''

prompt = '''Given the information above, your job is to create a plausible multiple choice question. Your response should be formatted like this: 'question;option1;*option2;option3;option4'. Include an asterisk to indicate the correct option. For example, with a paragraph about math, your response may look like this: '2+2=;2;3;*4;5'.'''

response = openai.ChatCompletion.create(
    model = 'gpt-3.5-turbo',
    messages = [
        {'role': 'system', 'content': content},
        {'role': 'system', 'content': prompt}
    ]
)

print(response.choices)
for i in response.choices:
    print(i.message.content)