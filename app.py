from flask import Flask, request
from flask_restful import Resource, Api
import base64
import boto3
from botocore.exceptions import ClientError
import os
import openai
import json


AWS_KEY = 'AKIA4HBH6HC6ZN6RHWHR'
AWS_SECRET = 'fmXyG/weujxAfPr5bEiNDcWT2G093Uw7trrlA6/E'


bucket = 'your_bucket_name_here'

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def post(self):
        filename = 'tst.jpg'

        b64_input = request.form['image']
        input_image = base64.b64decode(b64_input)
        with open(filename, 'wb') as img:
            img.write(input_image)

        # self.upload_file(filename, bucket)
        # text_count = self.detect_text(photo, bucket)

    def Converting(self):
        # cleaned up version

        openai.api_key = os.getenv("OPENAI_API_KEY")
        userInput = input("Enter the notes you want questions to be created for: ")

        response = openai.Completion.create(api_key="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", model="text-davinci-003", prompt="Convert my shorthand into complete sentences of my notes:\n\n" + userInput, temperature=0, max_tokens=256, top_p=1, frequency_penalty=0, presence_penalty=0)

        userSummary = response.choices[0].text
        print(userSummary)

        response = openai.Completion.create(api_key="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", model="text-davinci-003", prompt="Create a list of questions from my notes -\n\n" + userSummary + ": ", temperature=0, max_tokens=256, top_p=1, frequency_penalty=0, presence_penalty=0)

        userQuestions = response.choices[0].text
        print(userQuestions)

        response = openai.Completion.create(api_key="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", model="text-davinci-003", prompt="Create a list of answers for the questions based on my notes -\n\n" + "Questions: " + userQuestions + "\n\n My notes: " + userInput, temperature=0, max_tokens=256, top_p=1, frequency_penalty=0, presence_penalty=0)

        machineAnswers = response.choices[0].text
        print(machineAnswers)

        # mc
        response = openai.Completion.create(api_key="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", model="text-davinci-003", prompt="Create four possible answer choices to each question below based on my notes and the questions, with only one answer choice answering the question correctly. Print the correct answer choice at the end of each question. \n\n" + "Questions: " + userQuestions + "\n\n My notes: " + userInput, temperature=0, max_tokens=256, top_p=1, frequency_penalty=0, presence_penalty=0)

        machMC = response.choices[0].text
        print(machMC)


    def converttojson(self):
	my_string = '{"title": splitlines(userQuestions), "answers": splitlines(machineAnswers)"}'


        # json_output = format out of openai
        # return json_output
	return my_string


