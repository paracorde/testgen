import openai

content = '''The Chicago Cubs are an American professional baseball team based in Chicago. The Cubs compete in Major League Baseball (MLB) as part of the National League (NL) Central division. The club plays its home games at Wrigley Field, which is located on Chicago's North Side. The Cubs are one of two major league teams based in Chicago; the other, the Chicago White Sox, are a member of the American League (AL) Central division. The Cubs, first known as the White Stockings, were a founding member of the NL in 1876, becoming the Chicago Cubs in 1903.

'''

prompt = '''Given the information above, your job is to create a plausible multiple choice question with the correct choice repeated at the end. Your response should be formatted like this: 'question;option1;option2;option3;option4;correctOption'. For example, with a paragraph about math, your response may look like this: '2+2=;2;3;*4;5;4'''

response = openai.ChatCompletion.create(
    model = 'gpt-3.5-turbo',
    messages = [
        {'role': 'system', 'content': content},
        {'role': 'user', 'content': prompt}
    ]
)

# print(response.choices)
# print(response.choices[0].str())
print(response.choices[0].message.content)
genResponse = response.choices[0].message.content
genResponseList = response.choices[0].message.content.split(";")
print(genResponseList[0])
# print(response)
# for i in response.choices:
    # print(i.message.content)


quizInfo = dict([
    ("question", genResponseList[0]),
    ("options", genResponseList[1:len(genResponseList)-1]),
    ("correct", genResponseList[len(genResponseList)-1]),
])
print(quizInfo["options"])