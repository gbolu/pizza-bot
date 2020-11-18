from flask import Flask, request, session
from dotenv import load_dotenv
import requests, os
from twilio.twiml.messaging_response import MessagingResponse
from utils import *

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY')

# The main endpoint where messages arrive
@app.route('/pizza', methods=['POST'])
def pizza():
    if 'user' not in session:
        session['user'] = request.values.get('From').removeprefix('whatsapp:')

    command = request.values.get('Body', '').lower()
    parse_command(command=command)
    twilResponse = MessagingResponse()
    message = twilResponse.message()
    resp = message.body('Pizza party coming up!')

    return str(resp)

if __name__ == '__main__':
    app.run()