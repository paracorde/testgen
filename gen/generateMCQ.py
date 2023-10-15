import openai
prompt = '''Given the information above create a plausible multiple choice question with 4 choices and the index of the correct choice at the end. Do this all in a single line without option letters. Ensure your response is always formatted like this: 'question;option1;option2;option3;option4;indexCorrectOption'.  For example, with a paragraph about math, your response may look like this: '2+2=;2;3;4;5;2'''
promptAgain = '''Give me one more question based on the same information as above with the same formatting'''

def generateMCQ(notes,numQs):
    chatlog = [{'role': 'system', 'content': notes}, #stores all previous inputs and outputs of the interaction with the bot
            {'role': 'user', 'content': prompt}]
    response = openai.ChatCompletion.create(     #Getting the reponse from the bot using the prompt and the content stored under notes
        model = 'gpt-3.5-turbo',
        messages = [
            {'role': 'system', 'content': notes},
            {'role': 'user', 'content': prompt}
        ]
    )


    genResponse = response.choices[0].message.content #This represents the content of the output that the model returns i.e. The first choice object in the list of choice objects which the model returns after it is given the prompt. The content is represented as a long single string of the question, the options, and the index of the correct answer (index starting at 1) seperated by semicolons
    genResponseList = response.choices[0].message.content.split(";") #This splits the output using the delimeter ';' into a list of strings

    chatlog.append({'role': 'assistant', 'content': genResponse}) #Adding the bot's response to chatlog


    quizInfo = dict([ #A dictionary of the question, options, and index of the correct option in options list
        ("question", genResponseList[0]), #The first element in the list of strings represents the question
        ("options", genResponseList[1:-1]), #The rest of the  elements in the list of strings, APART FROM THE LAST ELEMENT, represent the possible answers
        ("correct", int(genResponseList[-1])-1), #The last element is a string which is the index of the correct option from the array of options. It is casted to an int because it is originally a string.
    ])
    quizInfos = [quizInfo] #Adding the dictionary to a list of all of the dictionaries for each question that has been generated
    
    #Generating more questions withe previous chatlog 
    for i in range(numQs-1): # Generating numQs-1 more questions (since 1 has already been generated)
        chatlog.append({'role': 'user', 'content': promptAgain}) #We only pass in a simpler new prompt since the model remembers the content (notes) and the original prompt through the chatlog which is passed in below
        response = openai.ChatCompletion.create(
            model = 'gpt-3.5-turbo',
            messages = chatlog
        )
        genNextResponse = response.choices[0].message.content 
        genNextResponseList = response.choices[0].message.content.split(";")
    
        chatlog.append({'role': 'assistant', 'content': genNextResponse})

        quizInfoNext = dict([
        ("question", genNextResponseList[0]), 
        ("options", genNextResponseList[1:-1]), 
        ("correct", int(genNextResponseList[-1])-1), 
    ])
    quizInfos.append(quizInfoNext)
    return quizInfos # returns a list of all the dictionaries from every generated response


