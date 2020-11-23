from flask import Flask, request, session
from dotenv import load_dotenv
import requests, os, googlemaps
from twilio.twiml.messaging_response import MessagingResponse 
from pprint import pprint

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
        msg.body(quote)
        responded = True

    else:
        if 'user' in session:
            if 'location' not in session:
                # save the location of the user in order
                session['location'] = incoming_msg

                # convert incoming location to http friendlu
                location = str(incoming_msg).replace(' ', '+')

                # grab coordinates of user location
                r = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={googleApiKey}')
                if r.status_code == 200:
                    geo_details = r.json()['results'][0]['geometry']['location']
                    latitude = geo_details['lat']
                    longitude = geo_details['lng']    

                    # check for available pizza places within 5km
                    r = requests.get(f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius=5000&keyword=pizza&key={googleApiKey}')
                    if r.status_code == 200:
                        places = [place for place in r.json()['results'] if place['opening_hours']['open_now']]
                        if places != []:
                            for place in places:
                                if place['opening_hours']['open_now']:
                                    pprint(place["name"])
                                    # msg.body(f'{place["name"]}')
                        else:
                            pass

                else:
                    msg.body('Could not find your location. Please try again.')
                responded = True

    if not responded:
        session.clear()
        msg.body('Invalid command! Please try starting with the command: \'pizza\'')
    return str(resp)


if __name__ == '__main__':
    app.run(debug=False)