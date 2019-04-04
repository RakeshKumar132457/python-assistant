#Importing
import speech_recognition as sr
import pyttsx3
from pygame import mixer
import time
import webbrowser
import wikipedia
import wolframalpha
import mysql.connector
from contextlib import suppress
import subprocess
import os
import requests, json 


mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "",
    database = "appointments"
     )

#Initialize
mixer.init()
engine = pyttsx3.init()
engine.setProperty('rate',140)
volume = engine.getProperty('volume')
engine.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')

def speak(querry):
    engine.say(querry)
    engine.runAndWait()
    time.sleep(2)

def opening_browser(query):
    request = webbrowser.open("http://www.google.com/search?q="+query)   
    return request

def wikipedia_api(query):
    result = wikipedia.summary(query,sentences=3)
    return result

def wolframalpha_api(my_input):
    app_id = "WOLFRAMALPHA API HERE"
    client = wolframalpha.Client(app_id)
    res = client.query(my_input)
    answer = next(res.results).text 
    return answer
    
class Appointments:
 
    def create_db(self):
        mycursor = mydb.cursor()
        mycursor.execute("CREATE DATABASE IF NOT EXISTS appointments;")
        mycursor.execute('''CREATE TABLE IF NOT EXISTS aptment(
                name varchar(20),
                date_aptment date,
                remarks varchar(200)
                );''')
    def insert_data(self,name,a_date,remarks):
        mycursor = mydb.cursor()
        sql = "insert into aptment (name,date_aptment,remarks) values (%s,%s,%s)"
        var = (name,a_date,remarks)
        mycursor.execute(sql,var)
        mydb.commit()
        print("Apointment set")
    
    def get_data(self):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM aptment")
        myresult = mycursor.fetchall()
        for x in myresult:
            print(x)
            
def search_program(program):
    dir_path = os.path.dirname(os.path.realpath('C:\*')) 
    for root, dirs, files in os.walk(dir_path): 
        for file in files:  
            if program in file: 
                return (root+'/'+str(file))
            
def opening_program(querry):
    subprocess.Popen(str(querry))
    
def google_maps(query):  
    api_key = 'GOOGLEMAPS API HERE'
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
    r = requests.get(url + 'query=' + query +'&key=' + api_key) 
    x = r.json() 
    y = x['results'] 
    for i in range(len(y)): 
        print(y[i]['name']) 
    

print("Welcome to enhanced personal assistant.....")
print("Enter your querry or speak up to get the results")
print("Say 'QUIT' to exit the Assitant")
print("")

while True:
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please wait. Calibrating microphone...")
        r.adjust_for_ambient_noise(source, duration=1)
        print("Say Something..")
        audio = r.listen(source,phrase_time_limit=5)
 
    try:
        response = r.recognize_google(audio)
        print("You said : " , response,)
        if 'appointment' in response:
            appt = Appointments()  
            
            if 'set' in response:
                name = input("Enter the name : ")
                date = input("Enter the date in YYYY/MM/DD formate : ")
                remarks = input("Enter the remarks : ")
                appt = Appointments()  
                appt.create_db()
                appt.insert_data(name,date,remarks)
                engine.say("Appointment set ")
                engine.runAndWait()
            elif 'show' in response:
                appt.get_data()
                
        elif 'alarm' in response:
            set_time = input("Enter time in HH:MM fomate : ")
            current_time = time.strftime("%H:%M")
            if(current_time == set_time):
                mixer.music.load("alarm.mp3")
                mixer.music.play()
                time.sleep(10)
                mixer.music.stop()    
                
        elif 'search' in response:
            pro = input("Enter the program you want to search with extension : ")
            search_program(pro)
            
        elif 'open' in response:
            op = input("Enter which program you want to enter with extension : ")
            path = search_program(op)
            opening_program(path)
            
        elif 'find' in response:
            q = input("Enter to search places : " )
            google_maps(q)
                
        with suppress(Exception):
            result = wolframalpha_api(response)
            print("Here is result for your querry : \n",response)
            print(result)
            speak(result)
            print("\n")
            
        with suppress(Exception):
            wiki_result = wikipedia_api(response)
            print("This is what wikipedia says about : ", response )
            print(wiki_result)
            speak(wiki_result)
            
        with suppress(Exception):
            opening_browser(response)
        
    except sr.UnknownValueError:
        print("Could not understand audio")
        continue
    except sr.RequestError as e:
        print("Error; {0}".format(e))
