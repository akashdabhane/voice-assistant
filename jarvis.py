import pyttsx3  # for voice of program
import speech_recognition as sr  # for listening to user's voice
import datetime  # for date and time
import wikipedia  # for wikipedia search
import webbrowser  # to open web browser
import os
import smtplib
import openai  # openai library for generating answers
import subprocess  # to get installed apps on system
import platform
import psutil  # to get information of apps installed on system
import requests  # to get information by api request
import json     # to deal with json data

# todo: tell him to open youtube/google/anything, and search something on opened website

openai.api_key = "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"

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")

    speak("I am your JARVIS, please tell me how may I help you.")


def takeCommand():
    # It takes microphone input from the user and return string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said : {query} \n")

    except Exception as e:
        # print(e)
        print("Say that again please...")
        return "None"

    return query


# using openai to response
def generate_gpt_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=400,
        n=1,
        stop=None,
        temperature=0.5,
    )
    print(response)
    return response["choices"][0]["text"]


# send email function
def sendEmail(to, content):
    print("Sending email...")
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login("youremail@gmail.com", "your-password")
    server.send("youremail@gmail.com", to, content)
    server.close()


# list of installed apps on system
def get_installed_apps():
    installed_apps = {}

    # Iterate through all running processes
    for proc in psutil.process_iter(["pid", "name"]):
        try:
            # Fetch the process details
            process_info = proc.info

            # Get the process name
            process_name = process_info["name"]

            # Get the process object to access additional information
            process = psutil.Process(process_info["pid"])

            # Get the executable path of the process
            executable_path = process.exe()

            # Add the process name and executable path to the dictionary
            installed_apps[process_name] = executable_path
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Handle exceptions that may occur during process retrieval
            pass

    return installed_apps


if __name__ == "__main__":
    wishMe()

    # Get the dictionary of installed applications and their executable paths
    # installed_apps_dict = get_installed_apps()

    # Print the list of installed applications and their executable paths
    # print("Installed Applications and their Executable Paths:")
    # for app, path in installed_apps_dict.items():
    #     print(f"{app}: {path}", "142")

    while True:
        query = takeCommand().lower()
        print(query)

        OpenQuery = query.split("open")
        print(OpenQuery)

        # logic for executing tasks based on query
        if "wikipedia" in query:
            speak("Searching wikipedia...")

            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query)

            speak("According to wikipedia")
            print(results)
            speak(results)

        elif "open" in query:
            OpenQuery = OpenQuery[1].strip().split(" ")
            webbrowser.open(f"{OpenQuery[0].strip()}.com")

        # open (use) app installed on system
        elif "use discord" in query:
            speak("discord")
            os.system(
                f"open C:/Users/Akash/AppData/Local/Discord/Update.exe --processStart Discord.exe"
            )

        elif "the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(strTime)
            speak(f"Sir, the time is {strTime}")

        elif "the date" in query:
            strDate = datetime.datetime.now().strftime("%d-%m-%Y")
            print(strDate)
            speak(f"Sir, the date is {strDate}")

        elif "quit" in query:
            speak("Thank you")
            break

        elif "play music" in query:
            music_dir = "D:\\songs"
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))

        # newsapi to get news
        elif "news" in query:
            url = (
                "https://newsapi.org/v2/top-headlines?"
                "country=in&"
                "apiKey=a3a93275fcc4458e85899f20b3c526d7"
            )
            response = requests.get(url)
            print(response.json())
            print(len(response.json()['articles']))
            
            for i in range(len(response.json()['articles'])):
                speak("Title")
                print(response.json()['articles'][i]['title'])
                speak(response.json()['articles'][i]['title'])
                
                speak("Description")
                print(response.json()['articles'][i]['description'])
                speak(response.json()['articles'][i]['description'])
                
                speak("Content")
                print(response.json()['articles'][i]['content'])
                speak(response.json()['articles'][i]['content'])
            
        
        # weather api   
        elif "weather" or "again" in query:
            print('weather')
            BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
            API_KEY = 'bc6aa613f85881873cc7a319655efa9e'
            CITY = "Mumbai"
            
            def kelvin_to_celsius_fahrenheit (kelvin):
                celsius = kelvin - 273.15
                fahrenheit = celsius * (9/5) + 32
                return celsius, fahrenheit


            url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY
            response = requests.get(url).json()

            temp_kelvin = response['main']['temp']
            temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)
            feels_like_kelvin = response['main']['temp']
            feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_fahrenheit(feels_like_kelvin)
            humidity = response['main']['humidity']
            # wind_speed = response['main']['speed']
            # description = response['main']['description']
            sunrise_time = datetime.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
            sunset_time = datetime.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])
            

            print(temp_kelvin, temp_celsius, feels_like_kelvin, feels_like_celsius, feels_like_fahrenheit, humidity)
            print(sunrise_time, sunset_time)
            # print(wind_speed, description, sunrise_time, sunset_time)
            
            speak(f"The temperature in {CITY} is {temp_celsius} degrees Celsius and {temp_fahrenheit} degrees Fahrenheit")
            speak(f"The temperature in {CITY} is feels like {feels_like_celsius:.2f} degrees Celsius and {feels_like_fahrenheit} degrees Fahrenheit")
            speak(f"Humidity in {CITY} is {humidity}%.")
            # speak(f"Wind speed in {CITY} is {wind_speed} m/s")
            # speak(f"General weather in {CITY} is {description}")
            speak(f"Sun rises in {CITY} is {sunrise_time} local time.") 
            speak(f"sun sets in {CITY} are {sunset_time} local time.")           

            

        # currently not working
        elif "email to akash" in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "akash@gmail.com"
                sendEmail(to, content)
                speak("Email has been sent")
            except Exception as e:
                print(e)
                speak("Sorry, I am not able to send the email")

        # open apps form the system if app is not installed then said

        else:
            try:
                response = generate_gpt_response(query)
                print("chatgpt says: " + response)
                speak(response)
            except Exception as e:
                # print(e)
                speak("Sorry, some error occurred")
