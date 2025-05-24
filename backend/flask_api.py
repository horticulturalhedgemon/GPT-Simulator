from flask import Flask, make_response, request
from openai import OpenAI
import requests, os

'''
#### Prompt
GET: fetch prompt from prompt file (separate script generates prompt from OpenAI
 - Response: prompt

#### Answer
POST: Submit answer
 - Request body: User-submitted answer
 - Task: Save answer to db, score with GPT-Zero
 - Response: GPT-Zero Score

#### Review
GET:
 - Request body: Answer id
 - Response: ChatGPT feedback
 
'''



app = Flask(__name__)
client = OpenAI()

@app.route("/prompt", methods=['GET'])
    # read prompt file
    # return prompt
def handlePrompt():
    #I still don't know why the path is relative to the project root directory and not the API's directory
    with open('backend/prompt.txt') as prompt_file:
        prompt = prompt_file.read()
        if len(prompt) == 0:
            return make_response("Prompt not found",500)
        else:
            return prompt;

@app.route("/answer",methods=['GET','POST'])
def handleAnswer():
    userid = request.args.get('userid')
    promptid = request.args.get('promptid')
    if request.method == 'POST':
        answer = request.args.get('answer')
        #take in user-submitted answer, run it through GPT-Zero, and return score
        url = "https://zerogpt.p.rapidapi.com/api/v1/detectText"

        payload = { "input_text": answer }
        headers = {
            "x-rapidapi-key": os.environ['ZEROGPT_API_KEY'],
            "x-rapidapi-host": "zerogpt.p.rapidapi.com",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)

        responseBody = response.json()
        #TODO: error handling
        if responseBody['success'] == True:
            return "AI Likelihood Score: " + str(responseBody['data']['is_gpt_generated'])
        else:
            return make_response("ZeroGPT API Failure",500)
    #find any answer from any user and prompt id
    elif request.method == 'GET':
        #take in user id and prompt id and return matching if found, error if not
        
        return "userid: " + userid + "\npromptid: " + promptid
    
@app.route("/review", methods=["GET"])
def getReview():
    #run user-submitted answer through ChatGPT and return its response
    global client
    answer = request.args.get('answer')
    prompt = request.args.get('prompt')
    response = client.responses.create(
        model="gpt-4o-mini",
        input="You are a perceptive, meticulous editor. Your task is to provide feedback on the provided answer to the provided prompt. Focus on making it more clear. Make sure to encourage the writer at the end.\n" +
        "Answer: " + answer + "\n Prompt: " + prompt)
    return response.output_text

if __name__ == "__main__":
    app.run(debug=True)