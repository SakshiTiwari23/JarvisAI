import speech_recognition as sr
import datetime
import os
import subprocess
import webbrowser
import openai
import pyttsx3
import requests
from config import apikey, apikey1

def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}")
        return query
    except:
        say("Sorry, I didn't understand. Please repeat.")
        return None

def get_weather(city):
    url = f"http://api.weatherapi.com/v1/current.json?key={apikey1}&q={city}"
    response = requests.get(url)
    data = response.json()

    if "error" in data:
        say("I couldn't find weather information for that location.")
    else:
        temp_c = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        say(f"The current temperature in {city} is {temp_c} degrees Celsius with {condition}.")

def weather_forecast():
    say("Which city's weather would you like to check?")
    city = take_command()  # listen to user's voice
    if city is not None:
        get_weather(city)
    else:
        say("I didn't catch the city name. Please try again.")


chatStr = ""

def chat(query, apikey):
    global chatStr
    openai.api_key = apikey

    # Build conversation string
    chatStr += f"Sakshi: {query}\nJarvis: "

    response = openai.chat.completions.create(
        model="gpt-4",  # or "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query}
        ],
        temperature=1,
        max_tokens=700,
        top_p=1
    )

    ai_reply = response.choices[0].message.content
    print(ai_reply)

    chatStr += ai_reply

    # Ensure the folder exists
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    # Save to file
    with open("Openai/conversation_log.txt", "a", encoding="utf-8") as f:
        f.write(f"Harry: {query}\nJarvis: {ai_reply}\n")

    # Make Jarvis speak
    say(ai_reply)

def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n ********************\n\n"

    try:
        response = openai.chat.completions.create(
            model="gpt-4",  # or "gpt-3.5-turbo" if you don't have GPT-4 access
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=1,
            max_tokens=700,
            top_p=1
        )
        # todo: Wrap this inside of a try catch block
        ai_reply = response.choices[0].message.content
        print(ai_reply)
        # say(ai_reply)
        text += ai_reply

        if not os.path.exists("Openai"):
            os.mkdir("Openai")

        # with open(f"Openai/prompt-{random.randint(1, 23425684848)}.txt", "w", encoding='utf-8') as f:
        with open(f"Openai/{''.join(prompt.split('intelligence')[1:])}.txt","w") as f:
            f.write(text)
    except Exception as e:
        print("Error communicating with OpenAI:", e)

def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Jarvis"

if __name__ == '__main__':
    print('PyCharm')
    say("Hello I am Jarvis A I")
    while True:
        print("Listening...")
        query = takeCommand()
        # todo : Add more sites
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"], ["instagram", "https://www.instagram.com"], ["github", "https://github.com/"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])

        # todo : Add a feature to play a specific song
        if "open music" in query:
            musicPath = "C:/Users/Sakshi/Downloads/wayudance - Time [NCS Release].mp3"
            os.startfile(musicPath)
        
        elif "what's the time" in query:
            strfTime = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"Sir the time is {strfTime}")

        elif "open vs code".lower() in query.lower():
            vscPath = r"C:\Users\Sakshi\AppData\Local\Programs\Microsoft VS Code\Code.exe"
            subprocess.Popen(vscPath)

        elif "open zoom".lower() in query.lower():
            zoomPath = r"C:\Users\Sakshi\AppData\Roaming\Zoom\bin\Zoom.exe"
            subprocess.Popen(zoomPath)

        elif "using artificial intelligence" in query.lower():
            ai(prompt=query)

        elif "Jarvis Quit".lower() in query.lower():
            exit()

        elif "weather".lower() in query.lower():
            weather_forecast()

        else:
            chat(query, apikey)





