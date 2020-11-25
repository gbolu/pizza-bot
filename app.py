import requests, os, googlemaps

from uuid import uuid4
from flask import Flask, request, session
from dotenv import load_dotenv
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
    incoming_msg = request.values.get('Body', '')
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if 'pizza' == incoming_msg:
        session.clear()
        #return a pizza quote
        quote = 'Pizza party coming right up! Please enter your address to view the closest restaurants delivering pizza.'
        if 'user' not in session:
            session['user'] = str(uuid4())
        msg.body(quote)
        responded = True

    else:
        if 'user' in session:
            if 'location' not in session:
                # save the location of the user in order
                session['location'] = incoming_msg

                # convert incoming location to http friendlu
                location = str(incoming_msg)
                prepped_location = location.replace(' ', '+')

                # grab coordinates of user location
                r = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={prepped_location}&key={googleApiKey}')
                if r.status_code == 200:
                    geo_details = r.json()['results'][0]['geometry']['location']
                    latitude = geo_details['lat']
                    longitude = geo_details['lng']                     

                    # check for available pizza places within 5km
                    r = requests.get(f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius=5000&keyword=pizza&key={googleApiKey}')
                    if r.status_code == 200:
                        results = r.json()['results']
                        if results == []:
                            resp.message("We're so sorry. There are no available locations close to you.")
                        else:
                            # pick top 3 pizza locations
                            places = [place for place in results if (place['opening_hours']['open_now'] or place['business_status'] == 'OPERATIONAL') and results.index(place) < 3]
                            if places != []:
                                msg.body("Here are the 3 closest available locations. Please select a location using the number in front of the location: ")
                                count = 1
                                for place in places:
                                    message = f"{count} - {place['name']} - {place['vicinity']}"
                                    resp.message(message)
                                    count += 1
                                order = Order(id=session['user'], orderLocation=location, possible_locations=places, phone_no=None)
                                order.store()
                                session['places'] = True
                            else:
                                resp.message("There are no open locations within 5km of you.")

                else:
                    msg.body('Could not find your location. Please try again.')
                responded = True
            else:
                if session['places']:
                    location_choice = int(incoming_msg)
                    order_dict = Order.getOrder(session['user'])
                    possible_locations = order_dict['possible_locations']
                    order = Order.orderFromStore(order_dict=order_dict)
                    responded = True
                    selected_location = possible_locations[location_choice]
                    order.orderLocation = selected_location
                    order.store()


    if not responded:
        session.clear()
        msg.body('Invalid command! Please try starting with the command: \'pizza\'')
    return str(resp)


if __name__ == '__main__':
    app.run(debug=False)