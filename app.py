"""from flask import Flask, request, send_file, session
import uuid
import os
import re
from utils.stt_utils import transcribe_audio
from utils.translate_utils import translate_text
from utils.gemini_nlu import get_gemini_response, reset_chat_session
from utils.tts_utils import synthesize_speech

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "your-secret-key")

@app.route("/")
def home():
    return "✅ AI Calling Agent (Pooja from Revino) is running."
    
@app.route("/voice", methods=["POST"])
def handle_voice():
    if "chat_active" not in session or not session["chat_active"]:
        reset_chat_session()
        session["chat_active"] = True


    filename = str(uuid.uuid4())
    input_path = f"{filename}_input.mp3"
    output_path = f"{filename}_response.mp3"

    audio_file = request.files["audio"]
    audio_file.save(input_path)

    # Step 1: Transcribe audio
    original_lang, user_text = transcribe_audio(input_path)
    print(f"🔍 Original language: {original_lang}, Text: {user_text}")


    # Step 2: Translate to English (if needed)
    if not original_lang.startswith("en"):
        translated_text = translate_text(user_text, src=original_lang, target="en")
    else:
        translated_text = user_text

    # Step 3: Get Gemini response
    response_english = get_gemini_response(translated_text)

    # Step 4: Translate back to original language (if needed)
    if not original_lang.startswith("en"):
        final_response = translate_text(response_english, src="en", target=original_lang)
    else:
        final_response = response_english

    # Step 5: Clean markdown (**bold**, etc.)
    final_response = re.sub(r'\*{1,2}', '', final_response)

    # Step 6: Convert response to speech
    audio_content = synthesize_speech(final_response, language_code=original_lang)
    with open(output_path, "wb") as f:
        f.write(audio_content)

    # 🧠 Debug logs
    print("🧠 Gemini (EN):", response_english)
    print("🔄 Final Translated Response:", final_response)
    print("📢 Speaking in:", original_lang)

    # Step 7: End session if conversation finished
    if any(phrase in user_text.lower() for phrase in ["bye", "thank you", "thanks", "goodbye", "अलविदा", "धन्यवाद", "i will let you know"]):
        session["chat_active"] = False
        final_response += "\nIt was great speaking with you. Have a wonderful day!"

    return send_file(output_path, mimetype="audio/mpeg")

if __name__ == "__main__":
    print("ENV:", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    app.run(host="0.0.0.0", port=8080, debug=True)"""


from flask import Flask, request, send_file, session
import os, uuid, re
from utils.stt_utils import transcribe_audio
from utils.translate_utils import translate_text
from utils.tts_utils import synthesize_speech
from utils.gemini_nlu import get_gemini_response, reset_chat_session

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "revino-secret")

@app.route("/")
def home():
    return "✅ Voice AI Agent is Running - Powered by Revino"

@app.route("/voice", methods=["POST"])
def handle_voice():
    if "chat_active" not in session or not session["chat_active"]:
        reset_chat_session()
        session["chat_active"] = True

    # 🎧 Save user audio
    filename = str(uuid.uuid4())
    input_path = f"{filename}_input.mp3"
    output_path = f"{filename}_response.mp3"
    request.files["audio"].save(input_path)

    # 🧠 Transcribe and detect language
    original_lang, transcript = transcribe_audio(input_path)
    print(f"🧾 FULL TRANSCRIPT: {transcript}")
    print(f"🧠 Final Detected Language: {original_lang}")

    # 🌍 Translate if not English
    if not original_lang.startswith("en"):
        text_for_nlu = translate_text(transcript, src=original_lang, target="en")
    else:
        text_for_nlu = transcript

    # 💬 Get response from Gemini (NLU)
    response_en = get_gemini_response(text_for_nlu)

    # 🌐 Translate back if needed
    if not original_lang.startswith("en"):
        response_final = translate_text(response_en, src="en", target=original_lang)
    else:
        response_final = response_en

    # ✂️ Clean unwanted markdown from Gemini
    response_final = re.sub(r'\*{1,2}', '', response_final)

    # 🗣️ Generate TTS
    audio_binary = synthesize_speech(response_final, language_code=original_lang)
    with open(output_path, "wb") as f:
        f.write(audio_binary)

    # 👋 End if user is done
    if any(kw in transcript.lower() for kw in ["bye", "thank you", "thanks", "अलविदा", "धन्यवाद", "goodbye"]):
        session["chat_active"] = False
        print("🔚 Ending conversation.")

    # 📢 Logs
    print("📨 Gemini Prompt Received:", text_for_nlu)
    print("🧠 Gemini Response:", response_en)
    print("🔄 Final Translated Response:", response_final)
    print("📢 Speaking in:", original_lang)

    return send_file(output_path, mimetype="audio/mpeg")

if __name__ == "__main__":
    print("🚀 AI Agent Starting...")
    app.run(host="0.0.0.0", port=8080, debug=True)
