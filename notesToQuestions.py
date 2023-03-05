#cleaned up version

import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
userInput = input("Enter the notes you want questions to be created for: ")

response = openai.Completion.create(api_key="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", model="text-davinci-003", prompt="Convert my short hand into a complete sentences of my notes:\n\n" + userInput, temperature=0, max_tokens=256, top_p=1, frequency_penalty=0, presence_penalty=0)
                              
userSummary = response.choices[0].text
print(userSummary)

response = openai.Completion.create(api_key="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", model="text-davinci-003", prompt="Create a list of questions from my notes -\n\n" + userSummary + ": ", temperature=0, max_tokens=256, top_p=1, frequency_penalty=0, presence_penalty=0)

userQuestions = response.choices[0].text
print(userQuestions)

response = openai.Completion.create(api_key="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", model="text-davinci-003", prompt="Create a list of answers for the questions based on my notes -\n\n" + "Questions: " + userQuestions + "/n/n My notes: " + userInput, temperature=0, max_tokens=256, top_p=1, frequency_penalty=0, presence_penalty=0)


machineAnswers = response.choices[0].text
print(machineAnswers)

#mc
response = openai.Completion.create(api_key="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", model="text-davinci-003", prompt="Create 4 possible answer choices to each questions below based on my notes and the questions, with only one answer choice answering the question correctly. Print the correct answer choice at the end of each question. \n\n" + "Questions: " + userQuestions + "/n/n My notes: " + userInput, temperature=0, max_tokens=256, top_p=1, frequency_penalty=0, presence_penalty=0)


machMC = response.choices[0].text
print(machMC)



