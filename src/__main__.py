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
from covid import Covid


import nltk
from nltk.corpus import stopwords # REMOVE STOP WORDS
from nltk.tokenize import word_tokenize

stopWords = stopwords.words('english')
stopWords.extend(['today', 'yesterday', 'tomorrow', 'search', 'send', "what's", 'tell', 'something', 'about', 'what', 'current', 'take'])

import re

regexEmail = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
regexUri = r'[A-Za-z0-9]+\.[a-z]+'

from sys import platform
import sys
import inflect # NUMBER TO TEXT

inflect = inflect.engine()
numtw = inflect.number_to_words

# TKINTER GUI ----------------
# import tkinter as tk
# from tkinter import ttk
from modules.tkinterAsync import Tkinter

try:
    with open(os.path.dirname(os.path.abspath(__file__)) + '/tkinter.setting.json', 'r') as reader:  # TKINTER SETTING ABS PATH
        tkinterSetting = json.load(reader) # CONVERT TEXT TO PYTHON DICTIONARY
        
except Exception as e:
    print(e)
    tkinterSetting = {
                        "activated": True,
                        "height": 300,
                        "width": 300
                    }

                    # DEFAULT VALUE IN CASE THE FILE DOEN'T EXIST

print(tkinterSetting)

OPENGUI = tkinterSetting['activated']

def AppGui(root, tk, ttk):
    root.title('Kronus.py Assistant')
    root.geometry(f'{tkinterSetting["width"]}x{tkinterSetting["height"]}')

    root.resizable(0, 0)

    global titleApp
    titleApp = tk.Label(root, text='Kronus')
    titleApp.config(font=('Helvatical bold',18))
    titleApp.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def printApp(text):
    if OPENGUI:
        global titleApp
        titleApp.config(text=text)

if OPENGUI:
    # IF THE OPTION IS ACTIVATED, WILL OPEN A WINDOW SECTION WITH CURRENT CONFIGURATION IN FILE
    APP = Tkinter(AppGui)


# ============================================================

# TEXT TO AUDIO
engine = pyttsx3.init()
voices = engine.getProperty('voices')

currentVoice = False

for voice in voices:
    if any(lang in voice.name for lang in ['english', 'English', 'en', 'EN', 'en-US', 'en-GB', 'US', 'GB']):
        currentVoice = voice
        break

engine.setProperty('voice', currentVoice.id if currentVoice else voices[0].id) # SELECT INDEX 0 IDF DOESN'T EXIST ENGLISH LANGUAGE
engine.setProperty('rate', 180)
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
        printApp('Listening...')
        # listener.pause_threshold = 1  FOR LOW SPEECH
        listener.adjust_for_ambient_noise(source)
        audio = listener.listen(source)

    try:
        print("Recognising...")
        printApp("Recognising...")
        query = listener.recognize_sphinx(audio) # NOT USING GOOGLE RECOGNIZER ANYMORE
        print('Command: {query}'.format(query = query))
        printApp(query)

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

    isInternetConnection()





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
        try:
            server = smtplib.SMTP(emailSetting['server'], emailSetting['port'])
            print('Conecting SMTP server...')
            server.ehlo()
            server.starttls()
            server.login(emailSetting['login']['username'], emailSetting['login']['password'])
        
        except Exception as e:
            talk('The server denied your connection')
            print(e)
            
            return False


        params = [0, 0, 0] # [to, subject, msg]
        paramsMSG = ['email', 'subject', 'message']



        for i in range(3):
            talk(f'Tell me the {paramsMSG[i]}')
            params[i] = getOrders().lower() # GET COMMANDS

            if(not params[i] or not re.match(regexEmail, params[0]) or 'manually' in params[i]):

                if (not params[i] or not re.match(regexEmail, params[0])):
                    talk("Sorry, I can't understand what did you say. Please enter manually the text")
                else:
                    talk('Please enter manually')

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
        if(isInternetConnection()):    # IN CASE THE SYSTEM HAVE INTERNET CONNECTION BUT RETURNS AN ERROR
            talk('Sorry something bad happens, please try again')


# OPEN WEBSITE
def openWebsite(query):
    if isInternetConnection():
        talk('Openning website...')
        print(query)

        # If no valid browser found then use webbrowser to automatically detect one
        try:
            supported_platforms = {'win32': 'windows-default', 'cygwin': 'cygstart', 'darwin': 'macosx'}
            if platform not in supported_platforms:
                browser_name = 'Automatically detected'
                browser_obj = wb.get()
            else:
                browser_name = supported_platforms[platform]
                if browser_name == 'cygstart':
                    # Cygwin requires us to register browser type (or export BROWSER='cygstart')
                    wb.register(browser_name, None, wb.GenericBrowser(browser_name))
                browser_obj = wb.get(browser_name)
        except wb.Error:
            pass

        print('Browser: '+browser_name)

        if not browser_obj.open(query):
            wb.open(query)


# OPEN MAPS
def openMap(query):
    talk('Opening the place on the map')

    url = f'https://maps.google.com/?q={query}'
    openWebsite(url)


def covid(query):
    # CONNECT API
    covid = Covid()
    if query:

        try:
            # COUNTRY
            if query.isdigit():
                data = covid.get_status_by_country_id(query)
            else:
                data = covid.get_status_by_country_name(query)

            txt = f'Right now {data["country"]} has: {numtw(data["confirmed"])} confirmed people, {numtw(data["active"])} current active people, {numtw(data["deaths"])} dead people by covid and {numtw(data["recovered"])} recovered'
            print(txt)
            talk(txt)

        except Exception as e:
            print(e)
            talk(f"Sorry, there isn't nothing about coronavirus {query}")
            pass
    else:

        data = sorted(covid.get_data(), key=lambda deaths: deaths['deaths'], reverse=True)[:3]

        confirmed = covid.get_total_confirmed_cases()
        active = covid.get_total_active_cases()
        recovered = covid.get_total_recovered()
        deaths = covid.get_total_deaths()

        txt = f'''
                    Updated from today, World coronavirus data: {numtw(confirmed)} confirmed people, {numtw(active)} current active people, {numtw(deaths)} dead people by covid and {numtw(recovered)} recovered.
                    
                    The first 3 country with more deaths are:

                    1. {data[0]['country']}: {numtw(data[0]['deaths'])} deaths
                    2. {data[1]['country']}: {numtw(data[1]['deaths'])} deaths
                    3. {data[2]['country']}: {numtw(data[2]['deaths'])} deaths

                '''
        print(txt)
        talk(txt)

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

    KeyActivated = bool(sys.argv[1]) if len(sys.argv) > 1 else False

    # WELCOME
    welcome()

    KronusActivated = True
    # WHEN THE BOT ASK SOME QUESTION STOP THE MAIN RECOGNITION
    SecondOrderActivated = False

    while KronusActivated:

        if(not SecondOrderActivated):
            if KeyActivated:
                # IF THE USER WANT TO USE THE KEYBOARD
                query = input().lower()
            else:
                # IF THE USER WANT TO USE THE VOICE
                query = getOrders().lower()  # GET COMMANDS

        else:
            query = ''

        # ------------------------------------------

        if any(str in query for str in ['kronus', 'cronus', 'canoes', 'canus', 'where are you', 'assistant', 'venus', 'krenus']):

            # RESPOND
            talk("Yes, i'm here")
            talk("What can I help you?")

        elif any(str in query for str in ['hi ', 'hello', 'good morning', 'good evening']):

            # WELCOME
            welcome()

        elif 'goodnight' in query:

            #
            talk('Have a good night')

        elif any(str in query for str in ['exit', 'bye', 'turn off']):

            talk('ok')

            if OPENGUI:
                APP.callback()
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

            date()  # GET THE CURRENT DATE

        elif 'time' in query:

            time()  # CURRENT TIME

        elif 'weather' in query:

            query = query.replace('weather', '')
            weather(removeWord(query))  # THE WEATHER

        elif 'joke' in query:

            joke()  # SOME FUNNY JOKES

        elif 'screenshot' in query:

            talk("Ok! I'm taking a screenshot")
            screenshot()  # SAVE AN SHOW SCREENSHOT

        elif any(str in query for str in ['wikipedia', "what's", 'what is', 'search']):

            query = query.replace('wikipedia', '')
            wikipedia(removeWord(query))  # SEARCH

        elif 'email' in query:

            # ACTIVATE SECOND ORDER
            SecondOrderActivated = True
            sendEmail()

            # FALSE
            SecondOrderActivated = False

        elif 'open' in query:

            query = query.replace('open', '')
            query = query.replace(' ', '')

            if re.match(regexUri, query):
                # OPEN URL
                openWebsite(removeWord(query))

        elif 'where is' in query:

            query = query.replace('where is', '')

            openMap(removeWord(query))

        elif any(str in query for str in ['coronavirus', 'covid']):

            # GET COVID DATA
            for str in ['coronavirus', 'covid']:
                query = query.replace(str, '')

            covid(removeWord(query))
