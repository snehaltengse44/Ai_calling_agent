from google.cloud import speech
import io

def transcribe_audio(audio_path):
    client = speech.SpeechClient()

    with io.open(audio_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-IN",  # primary
        alternative_language_codes=[
            "hi-IN", "bn-IN", "ta-IN", "te-IN", "gu-IN",
            "en-US","ml-IN", "kn-IN", "mr-IN", "pa-IN"
        ],
        enable_automatic_punctuation=True,
        model="latest_long"
    )

    response = client.recognize(config=config, audio=audio)

    if not response.results or not response.results[0].alternatives:
        return "en-US", ""

    result = response.results[0]
    transcript = result.alternatives[0].transcript.strip()

    # Use second word onward for script-based language detection
    words = transcript.split()
    check_text = " ".join(words)  # Use full transcript for detection

    print("🧪 Words:", words)
    print("🔍 Check Text for Script Detection:", check_text)
    print("🧾 FULL TRANSCRIPT:", transcript)

    # Detect Hindi (Devanagari) or English (ASCII)
    if any("\u0900" <= c <= "\u097F" for c in check_text):  # Hindi script
        detected_lang = "hi-IN"
    elif all(ord(c) < 128 for c in check_text):  # ASCII = English
        detected_lang = "en-IN"
    else:
        detected_lang = "en-IN"
    print("🧠 Final Detected Language:", detected_lang)

    return detected_lang, transcript