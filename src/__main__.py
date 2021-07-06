# KRONUS BOT
# Author: ZLL


import speech_recognition as sr # SPEECH TO TEXT
# IF IN TERMINAL THE speech_recognition SHOW AN ERROR YOU MUST INSTALL:
# 
# pip install pipwin (Windows)
# sudo apt-get install portaudio19-dev python-pyaudio (Linux, Ubuntu)
#
# THEN
#
# pip install PyAudio
# conda install pyaudio (Conda)


import pyttsx3 # TEXT TO SPEECH

# import pywhatkit # WHATSAPP FOR PYTHON
import datetime # FOR TIME REQUEST
import wikipedia as wk # ACCESS TO INFORMATION
import pyjokes # MAKE SOME JOKES
from modules.weather import Weather # IMPORT WEATHER API MODULES https://github.com/kadir014/weather.py
from modules.geoip import GeoIp # IMPORT MODULE BY ZLL
from modules.internet import isInternet # IMPORT MODULE BY ZLL

# MORE OPTIONS
import smtplib # EMAIL
import webbrowser as wb # SEARCH WEBSITES
import os # GET OS
import json
import string
import random
import subprocess
import pyautogui # CREATE GUI
from PIL import Image

import nltk
from nltk.corpus import stopwords # REMOVE STOP WORDS
from nltk.tokenize import word_tokenize

stopWords = stopwords.words('english')
stopWords.extend(['today', 'yesterday', 'tomorrow', 'search', 'send'])

import re

regexEmail = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


# ============================================================

# TEXT TO AUDIO
engine = pyttsx3.init()
voices = engine.getProperty('voices')

currentVoice = False

for voice in voices:
    
    if any(lang in voice.name for lang in ['english', 'English']):
        currentVoice = voice

engine.setProperty('voice', currentVoice.id if currentVoice else voices[0].id) # SELECT INDEX 0 IDF DOESN'T EXIST ENGLISH LANGUAGE
engine.setProperty('rate', 140)
engine.setProperty('volume', 1.0)


# FNC TO TALK
def talk(text):
    engine.say(text)
    engine.runAndWait()

# ===============================================================

def getOrders():  
    # OBTAIN AUDIO FROM MICROPHONE
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        # listener.pause_threshold = 1  FOR LOW SPEECH
        listener.adjust_for_ambient_noise(source)
        audio = listener.listen(source)

    try:
        print("Recognising...")
        query = listener.recognize_google(audio) # USE GOOGLE RECOGNIZER
        print('Command: {query}'.format(query = query))

    except Exception as e:
        print(e)
        query = '' # ENPTY RETURN

    return query


# =========================================================================


# GET TIME
def time():
    Time = datetime.datetime.now().strftime("%I:%M:%S %p")
    talk("The current time is {}".format(Time))

# GET DATE
def date():
    Year = datetime.datetime.now().year
    Month = datetime.datetime.now().month
    Day = datetime.datetime.now().day
    talk("The current date is {} of {} of {}".format(Day, Month, Year))


# GET WEATHER
def weather(query):
    query = query if query else GeoIp(0).city
    weather = Weather(query)

    if(weather.status):

        print(weather.owm)
        print(weather.wapi)

        talk(f'The weather today in {query}, {weather.country} is')
        talk(f'Temperature: {int(weather.temp)} centigrade, maximum temperature: {int(weather.temp_max)} centigrade, minimun temperature: {int(weather.temp_min)} centigrade, and its feel: {weather.temp_feelslike}	centigrade')
        talk(f'The humidity is {weather.humidity}, the cloud is {weather.cloudliness} and the wind speed is {weather.wind_speed} in {weather.wind_dir} direction')
        talk(f'The description of the weather from WeatherAPI is {weather.state_wapi}, and the description from OpenWeatherMap is {weather.state_owm}')

    else:
        talk(f'Sorry we can get any weather data from: {query}')
        

def geoip():
    
    ip = '0' # THE API AUTO DETECT THE CURRENT API

    geo = GeoIp(ip)

    talk(f'You are actually in {geo.country}, {geo.state}, {geo.city}')




# START WORKING
def welcome():
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour < 12:
        salute = "Good morning"
    elif hour >= 12 and hour < 18:
        salute = "Good afternoon"
    elif hour >= 18 and hour < 24:
        salute = "Good evening"
    else:
        salute = "Its been late, you should probably sleep now but anyways"
    
    # FIRST LINE
    talk(f"{salute}. Kronus at your services, what can i help you?")





# SEND A MAIL

## FIRST GET THE EMAIL SETTINGS

try:
    with open(os.path.dirname(os.path.abspath(__file__)) + '/email.setting.json', 'r') as reader:  # EMAIL SETTING ABS PATH
        emailSetting = json.load(reader) # CONVERT TEXT TO PYTHON DICTIONARY
        
except Exception as e:
    print(e)
    emailSetting = {
                        "server": "localhost",
                        "port": 587,
                        "login": {
                            "username": "user",
                            "password": "password",
                            "email": "deafult@localhost"
                        }
                    }

                    # DEFAULT VALUE IN CASE THE FILE DOEN'T EXIST


print(emailSetting)


def sendEmail():
    if emailSetting['activated']: # IF THE activated IS TRUE
        server = smtplib.SMTP(emailSetting['server'], emailSetting['port'])
        print('Conecting SMTP server...')
        server.ehlo()
        server.starttls()
        server.login(emailSetting['login']['username'], emailSetting['login']['password'])


        params = [0, 0, 0] # [to, subject, msg]
        paramsMSG = ['email', 'subject', 'message']



        for i in range(3):
            talk(f'Tell me the {paramsMSG[i]}')
            params[i] = getOrders().lower() # GET COMMANDS

            if(not params[i] or not re.match(regexEmail, params[0])):
                talk("Sorry, I can't understand what did you say. Please enter manually the text")

                params[i] = input() # CAN BE CHANGED TO GUI INPUT
            else:
                # IF USER WANT TO CLOSE
                if any(str in params[i] for str in ['exit', 'bye', 'turn off']):

                    return False
                
        # MESSAGE
        msg = 'Subject: {}\n\n{}'.format(params[1], params[2])

        
        server.sendmail(emailSetting['login']['email'], params[0], msg)
        server.close()
        talk('Message email sended!')
        print('Message email sended!')

    else:
        talk('You must enable this option and cofiguurate the email settings')



# MAKE SCREENSHOT
def screenshot():
    # MAKE SCREENSHOT
    img = pyautogui.screenshot()

    filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) + '.png'
    path =  'C:\\Users\\{}\\Pictures\\Screenshots\\'.format(os.getlogin())
    filepath = path + filename

    print('Image saved in: ' + filepath)
    img.save(filepath)

    image = Image.open(filepath)
    image.show()

    
# GET JOKES
def joke():
    talk(pyjokes.get_joke())


# WIKIPEDIA
def wikipedia(query):
    talk("Searching...")
    try:
        result = wk.summary(query, sentences=5)
        print(result)
        talk(result)
    except Exception as e:
        print(e)
        if(not isInternetConnection()):    # IN CASE THE SYSTEM HAVE INTERNET CONNECTION BUT RETURNS AN ERROR
            talk('Sorry something bad happens, please try again')



def isInternetConnection():

    if(not isInternet()):
        talk('Please make sure you have internet connection')
        return False
    else:
        return True


# REMOVE NOT IMPORTANT WORDS
def removeWord(query):

    queryArr = word_tokenize(query)

    filtered = [w for w in queryArr if not w.lower() in stopWords]

    query = " ".join(filtered)

    return query


if __name__ == '__main__':

    # WELCOME
    welcome()

    KronusActivated = True
    SecondOrderActivated = False # WHEN THE BOT ASK SOME QUESTION STOP THE MAIN RECOGNITION

    while KronusActivated:

        if(not SecondOrderActivated):
            query = getOrders().lower() # GET COMMANDS
        
        else:
            query = ''


        #------------------------------------------

        if any(str in query for str in ['kronus', 'cronus', 'canoes', 'canus', 'where are you', 'assistant']):

            # RESPOND
            talk("Yes, i'm here")
            talk("What can I help you?")

        elif query in ['hi', 'hello']:

            # WELCOME
            welcome()

        elif any(str in query for str in ['exit', 'bye', 'turn off']):

            # FALSE
            KronusActivated = False

        elif any(str in query for str in ['who are you', 'you name']):

            # TELL THE NAME
            talk("My name is Kronus, I'm your virtual assistant")

        elif any(str in query for str in ['where i am', "where i'm", 'current location', 'my location']):

            # TELL THE GEOLOCATION
            geoip()

        elif any(str in query for str in ['creator', 'created you']):

            talk('My creator is Zheng Lin Lei')


        elif 'date' in query:

            date() # GET THE CURRENT DATE

        elif 'time' in query:

            time() # CURRENT TIME

        elif 'weather' in query:

            query = query.replace('weather', '')
            weather(removeWord(query)) # THE WEATHER


        elif 'joke' in query:

            joke() # SOME FUNNY JOKES

        elif 'screenshot' in query:

            talk("Ok! I'm taking a screenshot")
            screenshot() # SAVE AN SHOW SCREENSHOT

        elif 'wikipedia' in query:
            
            query = query.replace('wikipedia', '')
            wikipedia(removeWord(query)) # SEARCH

        elif 'email' in query:

            # ACTIVATE SECOND ORDER
            SecondOrderActivated = True
            sendEmail()

            # FALSE
            SecondOrderActivated = False