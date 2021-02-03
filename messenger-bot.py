from flask import Flask, request
from pymessenger.bot import Bot

access_token = 'EAALD4kcWmEEBAJ1bfyOVlVs9M3Ai0L1XNqX54niCroO7c1FskXZBMrygaOMVVKwHEQHPl2irV0zyLCePMJGjEku9VJRutxjzREZBFUGzLNGDUtSLsKDFBJr2XeWvTip5CNCFJNNJDXFZAHz9FJPpzzNtSd94IHOZAbAAoXH34WUqFZAL8qgRV'
verify_token = 'firstbot'

bot = Bot(access_token)
app = Flask(__name__)


def verify_fb_token(token_sent):
    ## Verifies that the token sent by Facebook matches the token sent locally
    if token_sent == verify_token:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


def get_message_text():
    return "Hey, it looks like you're interested in HackRice! For more information, please visit http://hack.rice.edu"


## Send text message to recipient
def send_message(recipient_id, response):
    bot.send_text_message(
        recipient_id, response)  ## Sends the 'response' parameter to the user
    return "Message sent"


@app.route('/', methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        #Verify Token When Receive Messages
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #Handle POST Requests
    else:
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    #Facebook Messenger ID for user so we know where to send response back to
                    Recipeient_id = message['sender']['id']

                    # If User Send Text
                    if hackrise in message['message'].get('text').lower():
                        #Generate The Message
                        response_sent_text = get_message_text()
                        send_message(Recipeient_id, response_sent_text)

    return "Message Processed"


if __name__ == '__main__':
    app.run()
