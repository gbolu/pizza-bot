from flask import Flask, request, session
from dotenv import load_dotenv
import requests, os, googlemaps
from twilio.twiml.messaging_response import MessagingResponse, Redirect

from utils import Order

load_dotenv()

app = Flask(__name__)
googleApiKey = os.getenv('GOOGLE_API_KEY')
gmaps = googlemaps.Client(key=googleApiKey)

app.secret_key = os.getenv('SECRET_KEY')

# The main endpoint where messages arrive
@app.route('/', methods=['POST'])
def pizza():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if 'pizza' in incoming_msg:
        #return a pizza quote
        quote = 'Pizza party coming right up! Please enter your address to view the closest restaurants delivering pizza.'
        if 'user' not in session:
            session['user'] = request.values.get('From')
            new_order = Order()
            session['order'] = new_order
        msg.body(quote)
        resp.redirect('/location')
        responded = True

    if not responded:
        msg.body('Invalid command! Please try starting with the command: \'pizza\'')
    return str(resp)

@app.route('/location', methods=['POST'])
def getLocation():
    incoming_msg = request.values.get('Body', '').strip().lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if 'order' in session:
        location = str(incoming_msg).replace(' ', '+')
        r = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={googleApiKey}')
        if r.status_code == 200:
            geo_details = r.json()['geometry']['location']
            print(geo_details)
            msg.body(f'Your lat: {geo_details["lat"]}, your long: {geo_details["lng"]}')
        else:
            msg.body('Could not find your location. Please try again.')
        responded = True
    
    if not responded:
        msg.body('Invalid command')
    
    return str(resp)

if __name__ == '__main__':
    app.run(debug=False)