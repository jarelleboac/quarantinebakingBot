#Python libraries that we need to import for our bot
import random
from flask import Flask, request
from pymessenger.bot import Bot
import spoonacular as sp
import json
import requests


app = Flask(__name__)
ACCESS_TOKEN = 'EAANI58zW530BAEYCSGnpnonPV4ne80pbXl6JfYofrbz976puZBoSSKirGHvrIakhfh2lswZBvfxi5mPW9A4yfxHKJa3hACHADuvdUr9hOvzWy9CDIlILAGTq6shNSI9JVWZA0aDj25A1mKzjWPRF3foQxoht3RSmCi02ZAA14zvctzzwPJ8ZA'
VERIFY_TOKEN = 'yikes'
bot = Bot(ACCESS_TOKEN)

#added spoonacular api
url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/random"
querystring = {"number":"1","tags":"vegetarian,dessert"}
headers = {
    'x-rapidapi-key': "6149e1a2d1mshf54b509e116c55dp17a0bdjsn9eba0c1caa76",
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    #query= message['message'].get('text')
                    if(message['message'].get('text') == "I'm hungry!"):
                        response_sent_text = hungry()
                        send_message(recipient_id, response_sent_text)
                    if(message['message'].get('text') == "I want a random recipe!"):
                        response_sent_text = get_recipe()
                        send_message(recipient_id, response_sent_text)
                    if(message['message'].get('text') == "Thank you!"):
                        response_sent_text = thanks()
                        send_message(recipient_id, response_sent_text)
                    if(message['message'].get('text') == "ANOTHER ONE"):
                        response_sent_text = get_recipe()
                        send_message(recipient_id, response_sent_text)
                    if(message['message'].get('text') == "hello!"):
                        response_sent_text = get_message()
                        send_message(recipient_id, response_sent_text)
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response_sent_nontext = get_message()
                    send_message(recipient_id, response_sent_nontext)
    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def thanks():
    text= "No problem! 😋 If you want another, please type ANOTHER ONE! Otherwise, enjoy baking this new recipe. 🍴 🎉"

    return text 


#designate a specific message to send to hungry user
def hungry():
    text= "Let's get cooking, then!🍳Type your food preferences/ingredients separated by commas (i.e. 'apples,flour,sugar' 🌮) and we will recommend a recipe. Or say you want a random recipe! 💗"

    return text 
    
def get_recipe():
    response = requests.request("GET", url, headers=headers, params=querystring)
    #return "Here's a recipe for you 🎁 🥳!!!  " + data['title']
    #print(response)
    data = response.json()
    return "you got it! Here's a recipe for you 🎁 🥳!!!  " +"   \n"+"   \n"+"   \n"+data['recipes'][0]['title']+"   \n"+"   \n"+"   \n"+data['recipes'][0]['spoonacularSourceUrl']

#chooses a random message to send to the user
def get_message():
    sample_responses = ["Hello there 👋 , thanks for Boycotting Banana Bread! 🥰", 
    "Welcome to Boycott Banana Bread Bot! 👋 😊", 
    "Hello! 👋 Thanks for Boycotting Banana Bread!✨✨ Are you hungry? 🤩", 
    "We're greatful you're here! ✨✨ Thanks for Boycotting Banana Bread! Are you hungry? 🤩"]
    # return selected item to the user
    return random.choice(sample_responses)

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"


if __name__ == "__main__":
    app.run()

