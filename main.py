import pyttsx3            #for text-to-speech
import speech_recognition as sr    #for speech-to-text
import webbrowser                 #for opening sites
import datetime               
import subprocess              #for opening applications
import cv2                     #for camera
import threading
import os


# Initialize the text-to-speech engine
engine = pyttsx3.init()
# Replace with the correct voice ID if needed
default_id = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0'    #voice
engine.setProperty('voice', default_id)                          #set properties
engine.runAndWait()

def say(text):          
    engine.say(text)
    engine.runAndWait()

def takecommand():                         #take input
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            r.pause_threshold = 0.7
            audio = r.listen(source)                            #start microphone and take input
            query = r.recognize_google(audio, language="en-in")         #convert speech to text 
            print(f"user said: {query}")
            return query
        except sr.UnknownValueError:
            say("Sorry, I didn't catch that.")       #for no input
            return None
        except sr.RequestError:
            say("Sorry, there was a request error.")
            return None

class Camera: 
    def __init__(self):
        self.cap = None
        self.thread = None
    def show_cam(self):
        self.cap = cv2.VideoCapture(0)             #open camera
        if not self.cap.isOpened():
            print("Error: could not opoen camera")
            return
        while True:
        # Capture frame-by-frame
            ret, frame = self.cap.read()

        # If the frame is captured correctly, display it
            if not ret:
                break

            cv2.imshow('Camera Feed', frame)                       
            if cv2.waitKey(1)& 0xFF == ord('q'):
                break
        self.close()  

    def close(self):                                    #closing camera
        self.cap.release()
        self.cap = None
        cv2.destroyAllWindows()


if __name__ == '__main__':
    say("Hello, Friday here")
    camera = Camera()

    while True:
        print("Listening...")
        query = takecommand()              # taking command and store in query variable
        if query:
            sites = [
                ['youtube', 'https://www.youtube.com/'],
                ['instagram', 'https://www.instagram.com/'],
                ['chatgpt', 'https://chat.openai.com/'],
                ['facebook', 'https://www.facebook.com/'],
                ['whatsapp', 'https://web.whatsapp.com/'],
                ['wikipedia', 'https://www.wikipedia.org/'],
                ['spotify', 'https://open.spotify.com/']
            ]

            for site in sites:
                if f"open {site[0]}" in query.lower():
                    webbrowser.open(site[1])
                    say(f"Opening {site[0]} paras")
                    break  # Exit loop once the site is opened

            if "the time" in query.lower():
                hour = datetime.datetime.now().strftime("%H")
                minute = datetime.datetime.now().strftime("%M")
                say(f"Sir, the time is {hour} hours and {minute} minutes.")
            
            if "open brave" in query.lower():
                subprocess.Popen([r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"])
                say("brave opening sir")
            
            if "open mongo db" in query.lower():
                subprocess.Popen([r"C:\Users\khand\AppData\Local\MongoDBCompass\MongoDBCompass.exe"])
                say("Mongo DB opening sir")

            if "open my sql" in query.lower():
                subprocess.Popen([r"C:\Program Files\MySQL\MySQL Workbench 8.0\MySQLWorkbench.exe"])
                say("My Sql opening sir")

            if "open camera" in query.lower():
                say("opening camera")
                camera.thread = threading.Thread(target = camera.show_cam, args=())
                camera.thread.start()
            elif "close camera" in query.lower():
                say("closing camera")
                camera.close()
                if camera.thread is not None:
                    camera.thread.join()
                    camera.thread = None

            if "create a folder" in query.lower():
                say("enter name for the folder")
                name = input("")
                directory = rf"C:\Users\khand\OneDrive\Desktop\{name}"
                os.makedirs(directory, exist_ok=True)
                print(f"{name} folder created successfully")

            if "search for " in query.lower():
                query = '+'.join(query.split())
                search_url = f"https://www.google.com/search?q={query}"
                webbrowser.open(search_url)
