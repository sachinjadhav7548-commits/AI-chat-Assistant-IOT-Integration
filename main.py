import speech_recognition as sr
import os
import webbrowser
from google import genai
from config import apikey
import datetime
import pyttsx3

chatStr = ""
client = genai.Client(api_key=apikey)

def say(text):
    print(f"Brook: {text}")
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def chat(query):
    global chatStr
    print(chatStr)
    chatStr += f"Sohan: {query}\n Brook: "
    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=chatStr,
        )
        reply = response.text
        say(reply)
        chatStr += f"{reply}\n"
        return reply
    except Exception as e:
        error_msg = "Some Error Occurred. Sorry from Brook"
        print(e)
        say(error_msg)
        return error_msg

def ai(prompt):
    text = f"Gemini response for Prompt: {prompt} \n *************************\n\n"
    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
        )
        text += response.text
        if not os.path.exists("genai"):
            os.mkdir("genai")
            
        filename = f"genai/{''.join(prompt.split('intelligence')[1:]).strip() or 'output'}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)
        say("I have generated the response file for you sir.")
    except Exception as e:
        print(f"AI Error: {e}")
        say("Error generating AI response.")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Brook"

if __name__ == '__main__':
    print('Welcome to Brook A.I')
    say("Hi there, I am Brook A.I")
    while True:
        print("Listening...")
        query = takeCommand()
        
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"], ["github", "https://github.com"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])

        if "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            say(f"Sir time is {hour} hours and {min} minutes")

        elif "open facetime".lower() in query.lower():
            os.system(f"open /System/Applications/FaceTime.app")

        elif "open apple music".lower() in query.lower():
            os.system(f"open /System/Applications/Music.app")

        elif "open pass".lower() in query.lower():
            os.system(f"open /Applications/Passky.app")

        elif "using artificial intelligence".lower() in query.lower():
            ai(prompt=query)

        elif "brook quit".lower() in query.lower():
            say("Goodbye sir!")
            exit()

        elif "reset chat".lower() in query.lower():
            chatStr = ""
            say("Chat history reset.")

        else:
            print("Chatting...")
            chat(query)