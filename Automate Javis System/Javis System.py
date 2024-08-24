import threading
import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import tkinter as tk
from tkinter import messagebox
import requests
import os
import cv2

# Initialize speech recognition
recognizer = sr.Recognizer()
mic = sr.Microphone()

# Text-to-speech engine initialization
engine = pyttsx3.init()

# Flag to control the voice recognition thread
stop_event = threading.Event()
voice_thread = None
assistant_name = "Jarvis"

def speak(text):
    def _speak():
        engine.say(text)
        engine.runAndWait()
    root.after(0, _speak)

def get_weather():
    api_key = "your_api_key"  # Replace with your actual API key
    location = "your_location"  # Replace with your location
    response = requests.get(f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}")
    weather_data = response.json()
    return weather_data

def open_calculator():
    os.system("calc")

def open_spotify():
    webbrowser.open("spotify://")

def open_vscode():
    os.system("code")

def recognize_face():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # Face recognition logic here
    pass

def handle_command(command_text):
    command_text = command_text.lower()
    
    if "open google" in command_text:
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")
        
    elif "open youtube" in command_text:
        speak("Opening Youtube.")
        webbrowser.open("https://www.youtube.com")
        
    elif "play song" in command_text:
        speak("Khalid - Better (Official Video).")
        webbrowser.open("https://www.youtube.com/watch?v=x3bfa3DZ8JM")
        
    elif "time" in command_text:
        now = datetime.datetime.now()
        time_str = now.strftime("%H:%M:%S")
        speak(f"The current time is {time_str}.")
        
    elif "date" in command_text:
        now = datetime.datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        speak(f"Today's date is {date_str}.")
        
    elif "calculator" in command_text:
        open_calculator()
        
    elif "spotify" in command_text:
        open_spotify()
        
    elif "start voice recognition" in command_text:
        start_voice_recognition()
        
    elif "stop voice recognition" in command_text:
        stop_voice_recognition()
        
    elif "open vscode" in command_text:
        open_vscode()
        
    elif "open notepad" in command_text:
        speak("Opening Notepad.")
        os.system("notepad")
    
    elif "lock screen" in command_text:
        speak("Locking the screen.")
        os.system("rundll32.exe user32.dll,LockWorkStation")
    
    elif "shutdown" in command_text:
        speak("Shutting down the system.")
        os.system("shutdown /s /t 1")
    
    elif "restart" in command_text:
        speak("Restarting the system.")
        os.system("shutdown /r /t 1")
    
    elif "news" in command_text:
        speak("Opening the latest news.")
        webbrowser.open("https://news.google.com")
    
    else:
        speak(f"Command not recognized: {command_text}")


def recognize_speech_from_mic():
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
    
    while not stop_event.is_set():
        try:
            with mic as source:
                print("Listening for commands...")
                audio = recognizer.listen(source)

            try:
                response = recognizer.recognize_google(audio)
                print(f"Command: {response.lower()}")
                handle_command(response.lower())
            except sr.RequestError:
                print("API unavailable")
            except sr.UnknownValueError:
                print("Unable to recognize speech")
        except Exception as e:
            print(f"Error: {e}")

def send_command():
    user_input = entry.get()
    if user_input:
        print(f"Command received: {user_input}")
        handle_command(user_input.lower())
        speak(f"Executing command: {user_input}")
        entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please enter a command.")

def start_voice_recognition():
    global voice_thread
    if voice_thread is None or not voice_thread.is_alive():
        stop_event.clear()
        voice_thread = threading.Thread(target=recognize_speech_from_mic, daemon=True)
        voice_thread.start()
        speak("Voice recognition started.")
    else:
        speak("Voice recognition is already running.")

def stop_voice_recognition():
    stop_event.set()
    if voice_thread is not None:
        voice_thread.join()
        voice_thread = None
    speak("Voice recognition stopped.")

# GUI setup using Tkinter
root = tk.Tk()
root.title("JARVIS Assistant")
root.configure(bg="#f0f4f8")

frame = tk.Frame(root, bg="#e6e9ee")
frame.pack(pady=20, padx=10)

entry_label = tk.Label(frame, text="Enter your command:", bg="#e6e9ee", fg="#2c3e50")
entry_label.grid(row=0, column=0, padx=5)

entry = tk.Entry(frame, width=50, bg="#ffffff", fg="#2c3e50", bd=0, highlightthickness=0)
entry.grid(row=0, column=1, padx=5)

button = tk.Button(frame, text="Send", command=send_command, bg="#3498db", fg="white", activebackground="#2980b9", activeforeground="white")
button.grid(row=0, column=2, padx=5)

start_button = tk.Button(root, text="Start Voice Recognition", command=start_voice_recognition, bg="#2ecc71", fg="white", activebackground="#27ae60", activeforeground="white")
start_button.pack(pady=5)

stop_button = tk.Button(root, text="Stop Voice Recognition", command=stop_voice_recognition, bg="#e74c3c", fg="white", activebackground="#c0392b", activeforeground="white")
stop_button.pack(pady=5)

# Run Tkinter main loop
root.mainloop()
