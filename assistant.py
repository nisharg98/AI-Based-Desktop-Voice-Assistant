import tkinter as tk
from PIL import Image, ImageTk
import speech_recognition as sr
import pyttsx3
import datetime, time
import os
import webbrowser
import wikipedia
import random
import smtplib, ssl
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
import socket
import wolframalpha
import requests
import json
import pyowm
import pyjokes
import winshell
from ecapture import ecapture as ec
from urllib.request import urlopen

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
file = open("name.txt","r")
user_name = file.readline()
name = tk.Label(main, text="Welcome,"+user_name, bg="#01173e", fg="white", font=("",20), anchor="center")
name.pack()

# help function
def help_btn():
    help_window = tk.Tk()
    help_window.title("help and support")
    help_window.geometry("400x400")
    tk.Label(help_window, text="Help and Support", font=("",18)).place(x=100, y=30)
    tk.Label(help_window, text="1. Internet connection is required to access voice assistat.").place(x=10,y=100)
    tk.Label(help_window, text="2. To give voice command press the mic button in the application.").place(x=10,y=120)
    tk.Label(help_window, text="3. Please check your mic configuration for voice input.").place(x=10,y=140)
    tk.Label(help_window, text="4. Please check your speaker configuration for voice output.").place(x=10,y=160)
    tk.Label(help_window, text="5. To change user name press setting button on top right corner.").place(x=10,y=180)
    tk.Label(help_window, text="6. You can find suggestions to know more about commands.").place(x=10,y=200)

# help icon
help_icon = Image.open("help.png")
help_photo = ImageTk.PhotoImage(help_icon)
tk.Button(main, command=help_btn, image=help_photo, border=0, bg="black", activebackground="black").place(x=19, y=10)

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
        file1 = open("name.txt","w")
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

# history function
def history_btn():
    history = tk.Tk()
    history.title("History")
    history.geometry("500x500")
    history.config(bg="#f2efe6")
    file = open("history.txt","r")
    data = file.read()
    tk.Label(history, text=data, justify="left", font=("Trebuchet MS",11,"italic"), bg="#f2efe6", fg="#0b61bd").place(x=10)
    file.close()

# history icon
history = Image.open("history.jpg")
history_photo = ImageTk.PhotoImage(history)
tk.Button(main, command=history_btn, image=history_photo, border=0, bg="black", activebackground="black").place(x=625, y=80)

# suggestion
tk.Label(main, text="Suggestions:", bg="#001236", fg="white", font=("Calibri (Body)",12,"bold")).place(x=30,y=250)
tk.Label(main, text="1. Check Weather", bg="#001236", fg="white", font=("",10,"italic")).place(x=15,y=280)
tk.Label(main, text="2. Where is \"Ahmedabad\"", bg="#001236", fg="white", font=("",10,"italic")).place(x=15,y=300)
tk.Label(main, text="3. Play Music", bg="#001236", fg="white", font=("",10,"italic")).place(x=15,y=320)
tk.Label(main, text="4. Open \"Youtube\"", bg="#001236", fg="white", font=("",10,"italic")).place(x=15,y=340)
tk.Label(main, text="5. Calculate \"square of 2\"", bg="#001236", fg="white", font=("",10,"italic")).place(x=15,y=360)
tk.Label(main, text="6. Tell Me News", bg="#001236", fg="white", font=("",10,"italic")).place(x=15,y=380)
tk.Label(main, text="7. Write a Note", bg="#001236", fg="white", font=("",10,"italic")).place(x=15,y=400)
tk.Label(main, text="8. Show me Note", bg="#001236", fg="white", font=("",10,"italic")).place(x=15,y=420)
tk.Label(main, text="9. Search a File", bg="#001236", fg="white", font=("",10,"italic")).place(x=15,y=440)
tk.Label(main, text="10. Shutdown this PC", bg="#001236", fg="white", font=("",10,"italic")).place(x=15,y=460)

# say something label
say = tk.Label(main, text="Say Something", bg="#01173e", fg="white", font=("",20))
say.place(x=255,y=200)

# text to speech function
def speak(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()
    file = open("history.txt","a")
    file.write("\n"+command)
    file.close()

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
        #r.adjust_for_ambient_noise(source)
        r.energy_threshold = 4000
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio, language="en-in")
        speak("you said:"+text)
    except Exception as e:
        print(e)
        speak("say that again please")
        text = listen()
    return text

temp = 0
def temp_counter():
    global temp
    temp += 1

# initialization
def init():
    chk_internet()
    hour = int(datetime.datetime.now().hour)
    counter = temp
    if counter == 0:
        if hour>=0  and hour<12:
            speak("Hello "+user_name+", good morning")
        if hour>=12  and hour<18:
            speak("Hello "+user_name+", good afternoon")
        elif hour>=18 and hour<=24:    
            speak("Hello "+user_name+", good evening")
        speak("I am assistant how may i help you")
        temp_counter()

    text = listen()
    textlow = text.lower()
    action(textlow)

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
        #rno = random.randint(0,2)
        mdir = "C:\\Users\\rohit\\desktop\\music"
        songs = os.listdir(mdir)
        os.startfile(os.path.join(mdir, songs[0]))

    elif "mail" in text:
        speak("what's the message")
        message = listen()
        msg = MIMEMultipart()
        msg['Subject'] = "AI Based Desktop Voice Assistant Test Mail"
        msg.attach(MIMEText(message, 'plain'))
        mail = smtplib.SMTP("smtp.gmail.com", 587)
        mail.ehlo()
        mail.starttls()
        mail.login("nishargprajapati@gecg28.ac.in", "test@464")
        mail.sendmail("nishargprajapati@gecg28.ac.in", "nishargprajapati98@gmail.com", msg.as_string())
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

    elif "open chrome" in text:
        speak("Opening Google Chrome") 
        os.startfile("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe")
    
    elif "wikipedia" in text:
        speak("what do you want to search in wikipedia")
        query = listen()
        results = wikipedia.summary(query, sentences=2)
        url = wikipedia.page(query).url
        webbrowser.open(url)
        time.sleep(3)
        speak("according to wikipedia")
        speak(results)

    elif "weather" in text:
        speak("provide city name")
        city_name = listen()
        try:
            api_key = "30a009ff5a61bb5c03485abf62bf6fad"
            owm_obj = pyowm.OWM(api_key)
            obs_obj = owm_obj.weather_at_place(city_name)
            weather = obs_obj.get_weather()
            temp = weather.get_temperature('celsius')["temp"]
            humidity = weather.get_humidity()
            description = weather.get_detailed_status()
            reg = owm_obj.city_id_registry()
            city_id = reg.ids_for(city_name)
            url = "https://openweathermap.org/city/"+str(city_id[0][0])
            webbrowser.open(url)
            time.sleep(3)
            speak("current temperature is "+str(temp)+"celsius")
            speak("current humidity is "+str(humidity)+"%")
            speak("current weather description is "+description)
        except Exception as e:
            print(e)
            speak("City Not Found!, please provide correct city name")

    elif "news" in text:
        api_key = "b83225aa211a4f5c84002ef45d217086"
        try:
            jsonObj = urlopen("https://newsapi.org/v1/articles?source=the-times-of-india&sortBy=top&apiKey="+api_key)
            data = json.load(jsonObj)
            i = 1
            speak("here are some top news from the times of india")
            print("===============TIMES OF INDIA============\n")
            for item in data["articles"]:
                print(str(i) + ". " + item["title"] + "\n")
                print(item['description'] + '\n')
                speak(str(i) + ". " + item["title"] + "\n")
                i += 1
        except Exception as e:
            print(str(e))

    elif "calculate" in text:
        app_id = "AQXUVK-XUEUEKQ9VU" 
        client = wolframalpha.Client(app_id)
        indx = text.lower().split().index("calculate") 
        query = text.split()[indx + 1:] 
        res = client.query(' '.join(query)) 
        answer = next(res.results).text 
        speak("The answer is " + answer)

    elif "where is" in text:
        query=text.replace("where is","")
        location = query
        webbrowser.open("https://www.google.nl/maps/place/" + location + "")
        time.sleep(3)
        speak(location+" is found here")
    
    elif "write a note" in text:
        speak("What's in your mind?")
        note = listen()
        file = open("notes.txt","a")
        strTime = datetime.datetime.now().strftime("%D %H:%M:%S")
        file.write("\n\n"+strTime)
        file.write(" :- \n")
        file.write(note)
        file.close()
        speak("your note is saved thank you..")

    elif "show me note" in text:
        speak("Opening Notes") 
        os.startfile("notes.txt")

    elif "joke" in text:
        speak(pyjokes.get_joke())

    elif "empty recycle bin" in text:
        winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
        speak("Recycle Bin is cleared")

    elif "camera" in text or "take a photo" in text:
        ec.capture(0,"Camera","img.jpg")

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

    elif "search file" in text or "search a file" in text:
        speak("tell me the file name that you want to search")
        query = listen()
        count = 0
        for root, dirs, files in os.walk("C:\\Users\\rohit\\Desktop"):
            for file in files:
                if query in file:
                    if file.endswith(".txt"):
                        count += 1
                        print(root+"\\"+str(file))
                    elif file.endswith(".py"):
                        count += 1
                        print(root+"\\"+str(file))
                    elif file.endswith(".png"):
                        count += 1
                        print(root+"\\"+str(file))
                    elif file.endswith(".jpg"):
                        count += 1
                        print(root+"\\"+str(file))
                    elif file.endswith(".jpeg"):
                        count += 1
                        print(root+"\\"+str(file))
                    elif file.endswith(".java"):
                        count += 1
                        print(root+"\\"+str(file))
                    elif file.endswith(".pdf"):
                        count += 1
                        print(root+"\\"+str(file))
                    elif file.endswith(".docs"):
                        count += 1
                        print(root+"\\"+str(file))
                    elif file.endswith(".xlsx"):
                        count += 1
                        print(root+"\\"+str(file))

        if count == 0:
            print("file does not exist")
            speak("file does not exist")
        else:
            speak("file found")
            
    elif "shutdown" in text:
        speak("Do you want to shutdown this pc?")
        ans = listen()
        if "yes" in ans:
            speak("Your pc is shutting down shortly")
            os.system("shutdown /s /t 1")

    elif "exit" in text:
        speak("bye bye, have a nice day")
        main.destroy()
    
    else:
        speak("no results found!")

# mic Button
btn_img = Image.open("mic.jpg")
photo = ImageTk.PhotoImage(btn_img)
btn = tk.Button(main, text="Speak", command=init, width="50", height="50", image=photo, border=0, bg="#00286d", activebackground="#00286d")
btn.place(x=322,y=375)

main.mainloop()