from flask import Flask, request
from flask_restful import Resource, Api
import base64
import boto3
from botocore.exceptions import ClientError
import os
import openai
import json


AWS_KEY = 'AKIA3M65GZPGBZL6Y74H'
AWS_SECRET = '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'

bucket = 'swiftstudy'

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def post(self):
        filename = 'tst.jpg'
        b64_input = request.form['image']
        input_image = base64.b64decode(b64_input)
        with open(filename, 'wb') as img:
            img.write(input_image)

        self.upload_file(filename, bucket)
        print(filename)
        text_count = self.detect_text(filename, bucket)  # pass filename to detect_text
        printing = self.converttojson(*self.Converting(text_count))
        print(printing)

        return printing


    def upload_file(self, file_name, bucket, object_name=None):
        if object_name is None:
            object_name = os.path.basename(file_name)

        session = boto3.Session()
        s3_client = session.client('s3',aws_access_key_id=AWS_KEY,
                region_name = 'us-east-2',
                aws_secret_access_key=AWS_SECRET)

        try:
            response = s3_client.upload_file(file_name, bucket, object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def detect_text(self, photo, bucket):

        session = boto3.Session()
        client = session.client('rekognition',aws_access_key_id=AWS_KEY,
                    region_name = 'us-east-1',
                    aws_secret_access_key=AWS_SECRET)

        response = client.detect_text(Image={'S3Object': {'Bucket': bucket, 'Name': photo}})

        textDetections = response['TextDetections']
        print('Detected text\n----------')
        for text in textDetections:
            textininput = text['DetectedText']
            print(text['DetectedText'])
        return len(textDetections)

    def Converting(self, text_count):

        openai.api_key = os.getenv("OPENAI_API_KEY")
        userInput = input("Enter the notes you want questions to be created for: ")

        response = openai.Completion.create(api_key="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", model="text-davinci-003", prompt="Convert my shorthand into complete sentences of my notes:\n\n" + text_count, temperature=0, max_tokens=256, top_p=1, frequency_penalty=0, presence_penalty=0)

        userSummary = response.choices[0].text
        print(userSummary)

        response = openai.Completion.create(api_key="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", model="text-davinci-003", prompt="Create a list of questions from my notes -\n\n" + userSummary + ": ", temperature=0, max_tokens=256, top_p=1, frequency_penalty=0, presence_penalty=0)

        userQuestions = response.choices[0].text
        print(userQuestions)

        response = openai.Completion.create(api_key="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", model="text-davinci-003", prompt="Create a list of answers for the questions based on my notes -\n\n" + "Questions: " + userQuestions + "\n\n My notes: " + userInput, temperature=0, max_tokens=256, top_p=1, frequency_penalty=0, presence_penalty=0)

        machineAnswers = response.choices[0].text

        response = openai.Completion.create(api_key="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", model="text-davinci-003", prompt="Create four possible answer choices to each question below based on my notes and the questions, with only one answer choice answering the question correctly. Print the correct answer choice at the end of each question. \n\n" + "Questions: " + userQuestions + "\n\n My notes: " + userInput, temperature=0, max_tokens=256, top_p=1, frequency_penalty=0, presence_penalty=0)


        machMC = response.choices[0].text
        return userQuestions, machineAnswers

    def converttojson(self, questions, answers):
        my_string = '{"title": splitlines(questions), "answers": splitlines(answers)"}'


        return my_string

api.add_resource(HelloWorld, '/', methods = ['POST'])
