import pyttsx3
import os
import bs4, requests, datetime, webbrowser, GoogleNews
import speech_recognition as sr
import random
import time
import colorama
from colorama import Fore
import pyautogui
import pywhatkit as kit
import speedtest
import wikipedia
from dotenv import load_dotenv
import threading
import eel
import system_stats

load_dotenv()

# Initialize eel with the web folder
eel.init('web')

engine = pyttsx3.init('sapi5')
vocies = engine.getProperty('voices')
engine.setProperty('voices',vocies[1].id)

def gui_update_status(text, message=""):
    try:
        eel.set_assistant_state(text, message)()
    except:
        pass

def gui_log(msg):
    print(msg)

@eel.expose
def get_system_stats():
    return system_stats.get_all_stats()

def speak(audio):
    gui_update_status('SPEAKING', audio)
    gui_log(f'Speedy: {audio}')
    engine.setProperty("rate", 200)
    engine.say(audio)
    engine.runAndWait()
    gui_update_status('THINKING', "Awaiting Command...")

def takecommand():
    command1 = sr.Recognizer()
    standby_count = 0
    standby_threshold = 3

    with sr.Microphone() as source:
        gui_update_status('LISTENING', "Listening for command...")
        gui_log('Listening......')
        command1.pause_threshold = 0.5
        audio = command1.listen(source,phrase_time_limit=4)

        try:
            gui_update_status('THINKING', "Recognizing...")
            gui_log('recognizing......')
            command = command1.recognize_google(audio,language='en-in')
            gui_log(f'User: {command}')
            return command

        except Exception as e:
            gui_log(f"Error: {e}")
            standby_count += 1
            if standby_count >= standby_threshold:
                standby_count = 0
                speak("I didn't understand anything. Entering standby mode.")
                time.sleep(2)
                standby_mode()

            gui_log("say that again please....")
            return "none"

def chatbot(prompt):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        gui_log(f"Ollama Error: {e}")
        return "Sorry, I couldn't connect to Ollama. Please ensure the Ollama application is running on your PC."

def standby_mode():
    standby_name = "Speedy"
    command1 = sr.Recognizer()

    while True:
        with sr.Microphone() as source:
            gui_update_status('STANDBY', "Listening for wake word...")
            command1.pause_threshold = 0.5
            audio = command1.listen(source,phrase_time_limit=3)

            try:
                wake_word = command1.recognize_google(audio, language='en-in')
                if standby_name.lower() in wake_word.lower():
                    speak("Standby mode deactivated. How can I help you?")
                    return
            except Exception as e:
                pass
       
def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >=0 and hour <12 :
        speak("Good Morning!")
    elif hour >=12 and hour <18:
        speak("Good Afternoon!")
    else :
        speak("Good Evening!")

    speak("Hello! I am Speedy in your service. How can I help you?")

def close_program(program_name):
    try:
        os.system(f"taskkill /im {program_name}.exe /f")
        speak(f"{program_name} band ho gaya hai.")
    except Exception as e:
        speak("Kuch gadbad ho gayi, program nahi band hua.")

def continue_after_break():
    colorama.init(autoreset=True)
    speak("Do you want to continue? (yes/no): ")
    response = takecommand().lower()
    if response == "no":
        speak("Okay, taking a break. For how many minutes would you like to pause?")
        bt = takecommand()
        try:
            break_time = int(bt)
        except:
            break_time = 5
        remaining_time = break_time * 60
        speak(f"Sure! I'll be back after {break_time} minutes. Take your time!")

        while remaining_time > 0:
            if remaining_time == 70:
                speak("Just 1 minute and 10 seconds left.")
            if remaining_time == 10:
                speak("Only 10 seconds remaining. Get ready to resume!")
            time.sleep(1)
            remaining_time -= 1
            
        speak("Break time is over. I'm back!")
        return True
        
    elif "yes" in response or "continue" in response:
        return True
    elif "close" in response:
        speak("Okay! Closing the program. See you next time.")
        return False
    else:
        speak("Sorry, I didn't understand that. Do you want to continue? (yes/no): ")
        return continue_after_break()

def assistant_loop():
    time.sleep(2) # Give UI time to load
    wishme()
    while True:
        command = takecommand().lower()
        if command == "none":
            continue
    
        if "open" in command:
            command = command.replace("open","")
            pyautogui.hotkey("win", "s")
            time.sleep(0.5)
            pyautogui.typewrite(command)
            time.sleep(0.2)
            pyautogui.press("enter")
    
        elif "game" in command or "play game" in command or "play a game" in command:
            speak("great! i have 3 Games for you Would you like to play")
            while True:
                ak=takecommand()
                if "yes" in ak:
                    while ak == "yes":
                        speak("again great! What would you like to play Snake Water Gun, guess the Number or prices less KBC")
                        gm=takecommand()
                        if "snake" in gm or "water" in gm or "gun" in gm:
                            os.system(f"start vswg.py")
                            standby_mode()
                        elif "guess" in gm or "number" in gm:
                            os.system(f"start guno.py")
                            standby_mode()
                        elif"kbc" in gm or "quize" in gm:
                            os.system(f"start kbc.py")
                            standby_mode()
                        else:
                            speak(" i didn't understan speak again pls")
                            ak="yes"
                elif "no" in ak:
                    speak("no problem")
                    break
                else:
                    speak(" i didn't understan speak again pls")
    
        elif "intro" in command or "introduction" in command or "intradus" in command:
            speak("Hey there, I'm Speedy, your trusty AI companion, here to make your digital life a breeze!")
            speak(" i know you hsve many quetions for me like what i am? no! you know what i am what i can do!,how i work!, what is A I!,why my name speedy! etc")
            speak("What I Can Do!")
            speak("I can open programs, search the internet, open sites, and offer three entertaining games: Snake Water Gun, Guess the Number, and Prices-Less KBC.")
            speak("how i wor!")
            speak("I operate on a sophisticated algorithm that analyzes your input and responds with the most fitting reply.")
            speak("What is A I!")
            speak("Artificial Intelligence (AI) is not just a buzzword; it's a revolutionary force transforming every aspect of our lives.")
            speak("why my name is speedy!")
            speak("My name might be Speedy, but don't let that fool you—I'm here to bring a touch of humor to your day while being your efficient digital assistant.")
            speak("AI is not just the future; it's the present. From healthcare to finance, education to entertainment, AI is making waves.")
            speak("Why choose AI? Because I'm here to simplify your life, make tasks a breeze, and keep you entertained.")
            speak("So, buckle up, as we embark on this AI-driven journey together. Ready for the future? Let's make it happen, one command at a time!")
    
        elif "guess" in command or "number" in command:
            os.system(f"start guno.py")
            standby_mode()
    
        elif"kbc" in command or "quize" in command:
            os.system(f"start kbc.py")
            standby_mode()
    
        elif "snake" in command or "water" in command or "gun" in command:
            os.system(f"start vswg.py")
            standby_mode()
          
        elif "close" in command:
            parts = command.split(" ")
            if len(parts) > 1:
                program_name = parts[1]
                if program_name == "mycomputer":
                    close_program(r"C:\Windows\explorer.exe")
                elif program_name == "paint":
                    close_program(r"C:\Windows\System32\mspaint.exe")
                else:
                    close_program(program_name)
            else:
                speak("Program ka naam nahi mila.")
        elif "exit" in command or "bye" in command:
            speak("Alwida! See you next time.")
            break 
        elif "exhausted" in command or "tired" in command or "break" in command:
            if not continue_after_break():
                break
    
        elif "time" in command:
                time_now = datetime.datetime.now().strftime("%I:%M:%S %p")
                speak(time_now)
    
        elif "date" in command:
                date_now = datetime.datetime.now().strftime("%D")
                speak(date_now)
        elif "day" in command:
                day = datetime.datetime.now().strftime("%A")
                speak(day)
    
        elif "temperature" in command:
                q = command
                r = requests.get(f"https://www.google.com/search?q={q}")
                data = bs4.BeautifulSoup(r.text,"html.parser")
                temp = data.find("div",class_="BNeawe").text
                speak(f"the temperature outside is {temp}")
                
                speak("do you want another place temperature")
                place = takecommand()
                if "yes" in place or  "temperature" in place or "ya" in place:
                    speak("tell me the name of the place")
                    next_place = takecommand()
                    r = requests.get(f"https://www.google.com/search?q={next_place}")
                    data = bs4.BeautifulSoup(r.text,"html.parser")
                    temp = data.find("div",class_="BNeawe").text
                    speak(f"the temperature outside is {temp}")
                else:
                    speak("no problem!")
    
        elif "play" in command: 
                command = command.replace("play ","")
                kit.playonyt(command)
                speak(f"ok boss, playing {command}")
    
        elif "website" in command: 
            command = command.replace("website","").replace(" ","") 
            webbrowser.open(f"https://www.{command}.com")
            speak(f"ok boss, opening {command}")
            
        elif "search" in command: 
            command = command.replace("search","").replace(" ","") 
            webbrowser.open(f"https://www.{command}.com")
            speak(f"ok boss, opening {command}")
                
        elif "news of" in command: 
            command = command.replace("news of ","")
            new = GoogleNews.GoogleNews()
            speak(f"getting news of {command}")
            new.get_news(command)
            new.result()
            a = new.gettext()
            speak(a[1:5])
            
        elif "headlines" in command or "headline" in command: 
            new = GoogleNews.GoogleNews()
            speak("getting fresh headlines")
            new.get_news("headlines")
            new.result()
            a = new.gettext()
            speak(a[1:10])
        elif "speed test" in command or "test speed" in command:
            speed = speedtest.Speedtest()
            speak("checking")
            ul = speed.upload()
            ul = int(ul/800000)
            dl = speed.download()
            dl = int(dl/800000)
            speak(f"your upload speed is {ul} mbp s and your download speed is {dl} mbp s")
    
        elif "standby mode" in command or "standby" in command:
            standby_mode()
    
        elif 'wikipedia' in command or "tell about" in command:
            speak('seraching Wikipedia...')
            command=command.replace("wikipedia","") 
            results =  wikipedia.summary(command,sentences=2)
            speak('According to wikipedia')
            speak(results)
    
        else:
            speak(chatbot(command))      
    
        random_messages = [
            "Hope my assistance was helpful!","","","","","","",
            "Feel free to ask for more assistance.","","","","","","",
            "Is there anything else I can do for you?","","","","","","",
            "I hope you are enjoying our interaction.","","","","","","",
            "If you have any more questions, feel free to ask.""","","","","","",
        ]
        random_message = random.choice(random_messages)
        if random_message != "":
            speak(random_message)

if __name__ == '__main__':
    t = threading.Thread(target=assistant_loop, daemon=True)
    t.start()
    eel.start('index.html', size=(1000, 700))
