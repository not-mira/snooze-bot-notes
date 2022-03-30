def do_tweet():
    from requests_oauthlib import OAuth1Session
    import os
    imoprt json
    import time
    from time import gmtime, strftime
    
    # In your terminal set your environment variables by running the following code.
    # This saves the credentials needed to access Twitter's API to environment variables.
    # This information is collected from Twitter after registering as a developer and
    # collecting this information from the Twitter's developer console page
    
    #OAuth - method for users to get to their accounts w/o entering passwords and stuff
    #OAuth stands for Open Authentication
    
    # export 'CONSUMER_KEY'='<your_consumer_key>'
    # export 'CONSUMER_SECRET'='<your_consumer_secret>'
    # export 'ACCESS_TOKEN'='<your_access_token>
    # export 'ACCESS_TOKEN_SECRET'='<your_access_token_secret>'
    
    # These lines read the value of the Twitter credentials from the environment variables
    # and store them in python variables
    # (Code reads from pi/environment)
    
    consumer_key = os.environ.get("CONSUMER_KEY")
    consumer_secret = os.environ.get("CONSUMER_SECRET")
    access_token = os.environ.get("ACCESS_TOKEN")
    access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")
    
    # Create the string we want to tweet. Twitter will throw an error if you tweet the same
    # thing over and over again. The solution here is to add the current time to make
    # each tweet different
    
    # Basically just making Twitter think the account isn't a spam account or something
    # Even though it kinda is
    
    # Get the current time and format it as a string.
    stringtime = strftime("%a, %d %b %Y %H %M %S GMT", gmtime())
    
    # This is the basic string that will be tweeted.
    tweet_text = "Laz boy has hit the snooze button once more, and slumbers on. Pathetic."
    
    # Add the current time to the tweet to make it more unique
    tweet_text = tweet_text + " " + stringtime
    
    # Set th tweet_text as the JSON (JavaScript Object Notation) payload we want to pass on in the POST request to Twitter
    payload = {"text": tweet_text}
    
    # Setup Twitter OAuth1 authentication specifying
    # 1. Consumer key
    # 2. Access secret
    # 3. Access token
    # 4. Access secret
    # This is basically how Twitter knows who you are before running the API
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_srcret,
    )
    # Making the POST request to Twitter's API with the json payload string. Store
    # the return value in the response object.
    response = oauth.post(
        "https://api.twitter.com/2/tweets",
        json=payload,
    )
    
    # Anything other than HTTP 201 status is considered an error - print the error string
    if response.status_code !=201:
        raise Exception(
            "Request returned an error: {} {}".format(resopnse.status_code, response.text)
        )
        
    print("Response code: {}".format(response.status_code))
    
    # Save the response as JSON, and print it
    json_response = response.json()
    print(json.dumps(json_response, indent=4, sort_keys=True))


#This is the main loop - wait for button press (GPIO Pin 5). When pressed, send a tweet. This will only run on RPi
#TODO - curently calls GPIO pin 24 (to trigger an LED which is not currently on the board). Replace with writing something to the mini-display on RPI

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# LED (WIP)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)#Button to GPIO23
GPIO.setup(24, GPIO.OUT)  #LED to GPIO24

try:
    while True:
         button_state = GPIO.input(5)
         if button_state == False:
             GPIO.output(24, True)
             print('Button Pressed...')
             do_tweet()
             time.sleep(0.2)
         else:
             GPIO.output(24, False)
except:
    GPIO.cleanup()
