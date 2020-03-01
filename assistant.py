import tkinter as tk
from PIL import Image, ImageTk
import speech_recognition as sr
import pyttsx3
import datetime
import os
import webbrowser
import wikipedia
import random
import smtplib, ssl
import socket

# main window
main = tk.Tk()
main.title("AI Based Desktop Voice Assistant")
main.geometry("694x500")
main.resizable(width=False, height=False)
bg_img = Image.open("background.jpg")
background_image = ImageTk.PhotoImage(bg_img)
background_label = tk.Label(main, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# welcome name
file = open('name.txt','r')
user_name = file.readline()
name = tk.Label(main, text="Welcome,"+user_name, bg="#01173e", fg="white", font=("",20), anchor="center")
name.pack()

# change name function
def change_name():
    change = tk.Tk()
    change.title("Change User Name")
    change.geometry("350x130")
    tk.Label(change, text="Enter Name:").place(x=30, y=50)
    new_val = tk.Entry(change)
    new_val.place(x=105, y=50)
    
    # window refresh for updated name
    def change_value():
        user_name = new_val.get()
        file1 = open('name.txt','w')
        file1.write(user_name)
        file1.close()
        change.destroy()
        main.destroy() 
        exec(open("assistant.py").read(),globals())  
    tk.Button(change, text="Update", command=change_value).place(x=260, y=48)

# setting icon
setting = Image.open("setting.png")
setting_photo = ImageTk.PhotoImage(setting)
tk.Button(main, command=change_name, image=setting_photo, border=0, bg="black", activebackground="black").place(x=625 ,y=10)

# say something label
say = tk.Label(main, text="Say Something", bg="#01173e", fg="white", font=("",20))
say.place(x=255,y=200)

# text to speech function
def speak(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

# check internet connection
def chk_internet():
    IPaddress=socket.gethostbyname(socket.gethostname())
    if IPaddress=="127.0.0.1":
        speak("no internet connection!, please connect to internet")
        exit()

# voice input from user
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Say Something")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio, language="en-in")
        speak("you said:"+text)
        return text
    except Exception as e:
        print(e)
        speak("say that again please")
        listen()

# initialization
def init():
    chk_internet()
    hour = int(datetime.datetime.now().hour)    
    if hour>=0  and hour<12:
        speak("Hello"+user_name+", good morning")
    if hour>=12  and hour<18:
        speak("Hello"+user_name+", good afternoon")
    elif hour>=18 and hour<=24:    
        speak("Hello"+user_name+", good evening")
    speak("I am assistant how may i help you")
    text = listen().lower()
    action(text)

# do actions of users query
def action(text):
    if "how are you" in text:
        speak("I am fine")

    elif "setting" in text:
        os.system("start ms-settings:")

    elif "time" in text:
        tm = datetime.datetime.now().strftime(f"the date is %D and the time is %H:%M:%S")
        speak(tm) 

    elif "music" in text:
        rno = random.randint(0,9)
        mdir = "C:\\Users\\rohit\\Music"
        songs = os.listdir(mdir)
        os.startfile(os.path.join(mdir, songs[rno]))

    elif "mail" in text:
        speak("what's the message")
        message = listen()
        mail = smtplib.SMTP("smtp.gmail.com", 587)
        mail.ehlo()
        mail.starttls()
        mail.login("sender_mail", "password")
        mail.sendmail("sender_mail", "reciever_mail", message)
        mail.close()
        speak("mail has been sent successfully")

    elif "youtube" in text:
        speak("what do you want to search in youtube?")
        qr1 = listen()
        url = "https://www.youtube.com/results?search_query={}"
        search_url = url.format(qr1)
        webbrowser.open(search_url)
        speak("here are your search results")

    elif "google" in text:
        speak("what do you want to search in google?")
        qr2 = listen()
        url= "https://www.google.com/search?q={}"
        search_url = url.format(qr2)
        webbrowser.open(search_url)
        speak("here are your search results")
    
    elif "wikipedia" in text:
        speak("what do you want to search in wikipedia")
        query = listen()
        results = wikipedia.summary(query, sentences=2)
        url = wikipedia.page(query).url
        webbrowser.open(url)
        speak("according to wikipedia")
        speak(results)

    elif "word" in text:
        os.system("start winword")
        speak("microsoft word is opening")

    elif "excel" in text:
        os.system("start excel")
        speak("microsoft excel is opening")
    
    elif "powerpoint" in text:
        os.system("start powerpnt")
        speak("microsoft powerpoint is opening")

    elif "control panel" in text:
        os.system("control")
        speak("control panel is opening")

    elif "shutdown" in text:
        speak("Do you want to shutdown this pc?")
        ans = listen()
        if 'yes' in ans:
            speak("Your pc is shutting down shortly")
            os.system("shutdown /s /t 1")

    elif "exit" in text:
        speak("bye bye, have a nice day")
        exit()
    
    else:
        speak("no results found!")

# mic Button
btn_img = Image.open("mic.jpg")
photo = ImageTk.PhotoImage(btn_img)
btn = tk.Button(main, text="Speak", command=init, width="50", height="50", image=photo)
btn.place(x=322,y=375)

main.mainloop()