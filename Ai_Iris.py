from Ai_Models import Generate_pretrained_transformers
from Ai_Models import Main_Memories,Wheater_main,Auto_input_main
import pyttsx3 as ptx
import speech_recognition as sr
import time
import threading

response = Generate_pretrained_transformers()
Memories = Main_Memories()
Wheater = Wheater_main()
engine = ptx.init()

def speak_input () :
    recognition = sr.Recognizer()
    with sr.Microphone() as source:
        print("User :.... ")
        audio = recognition.listen(source)
    try :
        text = recognition.recognize_google(audio)
        return text 
    except sr.UnknownValueError:
        print("I,am thinking another things, so please wait.")
    except sr.RequestError :
        print("I,am thinking another things, so please wait.")

def voice_output (text) :
    voices = engine.getProperty('voices')
    rate = engine.getProperty('rate')
    engine.setProperty('voice',voices[1].id)
    engine.setProperty('rate',130)
    engine.say(text)
    engine.runAndWait() 

def get_wheater () :
    data = Wheater.info_wheaters()
    if data :
        return data 
    else : 
        return "sorry you have to connect internet to get information"

def interaction_input () :
    global user_respon 
    user_respon = speak_input()

def self_reflection () :
    global user_respon
    signal_input = Memories.from_memories_to_emosien_values()
    response = Auto_input_main(signal_input)
    user_respon = response.Automatic_input()

def get_input_for_Ai () :
    global user_respon
    user_respon = None 
    input_thread = threading.Thread(target=interaction_input)
    input_thread.start()
    input_thread.join(timeout=60)
    if user_respon is None :
        self_reflection()
    return user_respon
if __name__ == "__main__" :
    while True :
        input_user = get_input_for_Ai()
        if input_user.lower == 'wheater' :
            voice_output(get_wheater())
        elif input_user.lower == 'exit' or input_user.lower == 'quit' :
            break 
        Ai_response = response.Generated_Ai(input_user)
        voice_output(Ai_response)
        