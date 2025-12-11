import speech_recognition as sr
import win32com.client
import webbrowser
from openai import OpenAI
import os
import datetime
from config import apikey

# ------------------- AI Function -------------------

chatStr = ""


def chat(query):
    global chatStr
    print(chatStr)

    client = OpenAI(api_key=apikey)

    # remove the word "jarvis" from the prompt if spoken
    query = query.replace("jarvis", "").strip()

    chatStr += f"User: {query}\n Jarvis: "  # Fixed: removed "zz" typo
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Fixed: was "gpt-4.1-mini"
            messages=[{"role": "user", "content": chatStr}],
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        reply = response.choices[0].message.content
        say(reply)
        chatStr += f"{reply}\n"
        return reply

    except Exception as e:
        print("❌ Error ->", e)
        say("Sorry, I encountered an error")
        return None


def ai(prompt):
    client = OpenAI(api_key=apikey)

    # remove the word "jarvis" from the prompt if spoken
    prompt = prompt.replace("jarvis", "").strip()

    text = f"OpenAI response for Prompt: {prompt}\n*****************\n\n"

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Fixed: was "gpt-4.1-mini"
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500,  # Increased for longer responses
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        reply = response.choices[0].message.content
        print("\n🔵 AI:", reply)
        text += reply
        say(reply)

        if not os.path.exists("OpenAI"):
            os.mkdir("OpenAI")

        # -------- Safe File Name --------
        safe = "".join(x for x in prompt if x.isalnum() or x in (" ", "_")).strip()
        if len(safe) < 5:
            safe = "AI_Response_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        safe = safe.replace(" ", "_")
        # Limit filename length
        safe = safe[:100]
        # --------------------------------

        with open(f"OpenAI/{safe}.txt", "w", encoding="utf-8") as f:
            f.write(text)

        print(f"💾 Saved to: OpenAI/{safe}.txt")

    except Exception as e:
        print("❌ Error ->", e)
        say("Sorry, I encountered an error with AI processing")
        return None


# ------------------- Speaker -------------------
speaker = win32com.client.Dispatch("SAPI.SpVoice")


def say(text):
    try:
        speaker.Speak(text)
    except Exception as e:
        print(f"❌ Speech Error: {e}")


# ------------------- Speech Input -------------------
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎤 Listening...")
        r.pause_threshold = 1.0
        r.energy_threshold = 300  # Adjust based on environment
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"🗣 User said: {query}")
            return query
        except sr.WaitTimeoutError:
            print("⏰ Listening timeout")
            return "None"
        except sr.UnknownValueError:
            print("🤷 Could not understand audio")
            return "None"
        except Exception as e:
            print(f"❌ Error: {e}")
            return "None"


# ------------------- Main Program -------------------
if __name__ == "__main__":
    print("🤖 Jarvis AI Starting...")
    say("Hello Sir, I am your AI Assistant Jarvis. How can I help you?")

    while True:
        query = takeCommand()

        if query == "None":
            continue

        # Convert to lowercase for easier matching
        query_lower = query.lower()

        # Exit Command
        if any(word in query_lower for word in ["exit", "stop", "quit", "goodbye"]):
            say("Goodbye Sir, Have a nice day!")
            break

        # Websites
        sites = {
            "youtube": "https://www.youtube.com",
            "wikipedia": "https://en.wikipedia.org/wiki/Main_Page",
            "google": "https://www.google.com",
            "facebook": "https://www.facebook.com",
            "github": "https://github.com"
        }

        site_opened = False
        for site in sites:
            if f"open {site}" in query_lower:
                say(f"Opening {site} Sir...")
                webbrowser.open(sites[site])
                site_opened = True
                break

        if site_opened:
            continue

        # Music
        if "open music" in query_lower or "play music" in query_lower:
            musicPath = r"C:\Users\Imran Farhat\Downloads\flute-traditional-v1-251387.mp3"
            if os.path.exists(musicPath):
                say("Playing music for you Sir...")
                os.startfile(musicPath)
            else:
                say("Sorry, I could not find the music file")

        # Time
        elif "time" in query_lower:
            strfTime = datetime.datetime.now().strftime("%I:%M %p")
            say(f"The time is {strfTime}")

        # Date
        elif "date" in query_lower or "what day" in query_lower:
            strfDate = datetime.datetime.now().strftime("%A, %B %d, %Y")
            say(f"Today is {strfDate}")

        # --------- ADVANCED AI TRIGGER ---------
        elif ("using artificial intelligence" in query_lower) or \
                ("write" in query_lower and "letter" in query_lower) or \
                ("write" in query_lower and "email" in query_lower) or \
                ("generate" in query_lower):
            say("Processing your request using Artificial Intelligence...")
            ai(prompt=query)

        elif "jarvis quit" in query_lower:
            say("Shutting down Jarvis")
            break

        elif "reset chat" in query_lower:
            chatStr = ""
            say("Chat history has been reset")

        else:
            print("Chatting...")
            chat(query)