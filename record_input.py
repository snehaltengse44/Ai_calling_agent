import speech_recognition as sr
import requests
from pydub import AudioSegment
from pydub.playback import play

# 🎧 Play the MP3 response using PyDub
def play_response(filename="response.mp3"):
    audio = AudioSegment.from_file(filename)
    play(audio)

# 🎙️ Record user input from microphone
def record_input(filename="input.wav"):
    recognizer = sr.Recognizer()
    with sr.Microphone(sample_rate=16000) as source:
        print("🎙️ You: (speak now)")
        audio = recognizer.listen(source, timeout=15, phrase_time_limit=35)
    with open(filename, "wb") as f:
        f.write(audio.get_wav_data())
    print("🎧 Audio saved as:", filename)

# 📤 Send audio to agent and play the reply
def send_to_agent(filename="input.wav"):
    files = {'audio': open(filename, 'rb')}
    res = requests.post("http://localhost:8080/voice", files=files)
    with open("response.mp3", "wb") as f:
        f.write(res.content)
    play_response("response.mp3")

# 🔊 Trigger agent greeting once at start
def trigger_agent_greeting():
    print("🤖 Playing agent intro greeting...")
    res = requests.get("http://localhost:8080/greet")
    with open("response.mp3", "wb") as f:
        f.write(res.content)
    play_response("response.mp3")

# 🔁 Conversation loop
if __name__ == "__main__":
    print("✅ Starting AI voice agent...")
    
    #trigger_agent_greeting()  # ✅ Speak first without waiting for input

    while True:
        record_input()
        send_to_agent()
        print("🔁 Speak again or press Ctrl+C to exit\n")
