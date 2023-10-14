import openai


content = '''Throughout the club's history, the Cubs have played in a total of 11 World Series. The 1906 Cubs won 116 games, finishing 116-36 and posting a modern-era record winning percentage of .763, before losing the World Series to the Chicago White Sox ("The Hitless Wonders") by four games to two. The Cubs won back-to-back World Series championships in 1907 and 1908, becoming the first major league team to play in three consecutive World Series, and the first to win it twice. Most recently, the Cubs won the 2016 National League Championship Series and 2016 World Series, which ended a 71-year National League pennant drought and a 108-year World Series championship drought, both of which are record droughts in Major League Baseball.The 108-year drought was also the longest such occurrence in all major sports leagues in the United States and Canada. Since the start of divisional play in 1969, the Cubs have appeared in the postseason 11 times through the 2022 season.'''

prompt = '''Given the information above, your job is to create a plausible multiple choice question with 4 choices and the index of the correct choice at the end, with the indexes starting at 0. Your response should be formatted like this: 'question;option1;option2;option3;option4;indexCorrectOption'. For example, with a paragraph about math, your response may look like this: '2+2=;2;3;4;5;2'''

response = openai.ChatCompletion.create(
    model = 'gpt-3.5-turbo',
    messages = [
        {'role': 'system', 'content': content},
        {'role': 'user', 'content': prompt}
    ]
)


genResponse = response.choices[0].message.content #This represents the content of the output that the model returns i.e. The first choice object in the list of choice objects which the model returns after it is given the prompt.
genResponseList = response.choices[0].message.content.split(";") #This splits the output using the delimeter ';' into a list of strings
print(genResponseList[0])



quizInfo = dict([
    ("question", genResponseList[0]), #The first element in the list of strings represents the question
    ("options", genResponseList[1:-1]), #The rest of the  elements in the list of strings, APART FROM THE LAST ELEMENT, represent the possible answers
    ("correct", int(genResponseList[-1])), #The last element is a string which is the index of the correct option from the array of options. It is casted to an int because it is originally a string. 

])

print(quizInfo["options"])
print(quizInfo["correct"])

