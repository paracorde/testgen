import openai


content = '''Washington University in St. Louis (WashU, WUSTL or Washington University) is a private research university with its main campus in St. Louis County, and Clayton, Missouri. Founded in 1853, the university is named after George Washington. The university's 169-acre Danforth Campus is at the center of Washington University and is the academic home to the majority of the university's undergraduate, graduate, and professional students. '''

prompt = '''Given the information above create a plausible multiple choice question with 4 choices and the index of the correct choice at the end. Do this all in a single line without option letters. Ensure your response is always formatted like this: 'question;option1;option2;option3;option4;indexCorrectOption'.  For example, with a paragraph about math, your response may look like this: '2+2=;2;3;4;5;2'''
promptAgain = '''Give me one more question based on the same information as above with the same formatting'''
questionFRQprompt= '''Based on the information given above, create a short answer question prompt.'''
graderFRQprompt = '''You are a short answer question grader. Based on the short answer prompt given above along with the response given by the user above you must grade the response on a scale from 0-10 and then include an explanation of the grade. Ensure that your format looks like this: score;explanation'''
userSimAns = '''Oranges are citrus fruits'''
response = openai.ChatCompletion.create( #generating FRQ prompt using model passing in content and prompt
    model = 'gpt-3.5-turbo',
    messages = [
        {'role': 'system', 'content': content},
        {'role': 'user', 'content': questionFRQprompt}
    ]
)




genResponse = response.choices[0].message.content #This represents the content of the output that the model returns i.e. The first choice object in the list of choice objects which the model returns after it is given the prompt.
#genResponseList = response.choices[0].message.content.split(";") #This splits the output using the delimeter ';' into a list of strings
print(genResponse)


response2 = openai.ChatCompletion.create( #generating FRQ prompt using model passing in content and prompt
    model = 'gpt-3.5-turbo',
    messages = [
        {'role': 'assistant', 'content': genResponse},
        {'role': 'user', 'content': userSimAns},
        {'role': 'system', 'content': graderFRQprompt},
    ]
)

genResponse2 = response2.choices[0].message.content #This represents the content of the output that the model returns i.e. The first choice object in the list of choice objects which the model returns after it is given the prompt.
genResponse2List = response2.choices[0].message.content.split(";") #This splits the output using the delimeter ';' into a list of strings
FRQInfo = dict([
    ("grade", genResponse2List[0]), #The first element in the list of strings represents the question
    ("explanation", genResponse2List[1]), #The rest of the  elements in the list of strings, APART FROM THE LAST ELEMENT, represent the possible answers
])
print(genResponse2)
for key, value in FRQInfo.items():
    print(key, ":", value)


# quizInfo = dict([
#     ("question", genResponseList[0]), #The first element in the list of strings represents the question
#     ("options", genResponseList[1:-1]), #The rest of the  elements in the list of strings, APART FROM THE LAST ELEMENT, represent the possible answers
#     ("correct", int(genResponseList[-1])), #The last element is a string which is the index of the correct option from the array of options. It is casted to an int because it is originally a string. 

# ])
# print(genResponse)
# print(quizInfo["options"])
# print(quizInfo["correct"])


# def generateMCQ(notes,numQs):
    # chatlog = [{'role': 'system', 'content': notes},
    #         {'role': 'user', 'content': prompt}]
    # response = openai.ChatCompletion.create(
    #     model = 'gpt-3.5-turbo',
    #     messages = [
    #         {'role': 'system', 'content': notes},
    #         {'role': 'user', 'content': prompt}
    #     ]
    # )


    # genResponse = response.choices[0].message.content #This represents the content of the output that the model returns i.e. The first choice object in the list of choice objects which the model returns after it is given the prompt.
    # genResponseList = response.choices[0].message.content.split(";") #This splits the output using the delimeter ';' into a list of strings

    # chatlog.append({'role': 'assistant', 'content': genResponse})


    # quizInfo = dict([
    #     ("question", genResponseList[0]), #The first element in the list of strings represents the question
    #     ("options", genResponseList[1:-1]), #The rest of the  elements in the list of strings, APART FROM THE LAST ELEMENT, represent the possible answers
    #     ("correct", int(genResponseList[-1])-1), #The last element is a string which is the index of the correct option from the array of options. It is casted to an int because it is originally a string.
    # ])
    # quizInfos = [quizInfo]
    
    # #Generating more questions withe previous chatlog 
    # for i in range(numQs):
    #     chatlog.append({'role': 'user', 'content': promptAgain})
    #     response = openai.ChatCompletion.create(
    #         model = 'gpt-3.5-turbo',
    #         messages = chatlog
    #     )
    #     genNextResponse = response.choices[0].message.content #This represents the content of the output that the model returns i.e. The first choice object in the list of choice objects which the model returns after it is given the prompt.
    #     genNextResponseList = response.choices[0].message.content.split(";") #This splits the output using the delimeter ';' into a list of strings
    
    #     chatlog.append({'role': 'assistant', 'content': genNextResponse})

    #     quizInfoNext = dict([
    #     ("question", genNextResponseList[0]), #The first element in the list of strings represents the question
    #     ("options", genNextResponseList[1:-1]), #The rest of the  elements in the list of strings, APART FROM THE LAST ELEMENT, represent the possible answers
    #     ("correct", int(genNextResponseList[-1])-1), #The last element is a string which is the index of the correct option from the array of options. It is casted to an int because it is originally a string.
    # ])
    # quizInfos.append(quizInfoNext)
    # return quizInfos



# c= '''Washington University in St. Louis (WashU, WUSTL or Washington University) is a private research university with its main campus in St. Louis County, and Clayton, Missouri. Founded in 1853, the university is named after George Washington. The university's 169-acre Danforth Campus is at the center of Washington University and is the academic home to the majority of the university's undergraduate, graduate, and professional students. '''
# quiz  = generateMCQ(c)
# for key, value in quiz.items():
#     print(key, ":", value)


# c= '''Washington University in St. Louis (WashU, WUSTL or Washington University) is a private research university with its main campus in St. Louis County, and Clayton, Missouri. Founded in 1853, the university is named after George Washington. The university's 169-acre Danforth Campus is at the center of Washington University and is the academic home to the majority of the university's undergraduate, graduate, and professional students. '''
# quiz  = generateMCQ(c,1)
# print((quiz[0])['question'])
# print((quiz[0])['options'])
# print((quiz[0])['correct'])
# print((quiz[1])['question'])
# print((quiz[1])['options'])
# print((quiz[1])['correct'])
# for key, value in quiz.items():
#     print(key, ":", value)



