from google.cloud import translate_v2 as translate
import os
print("ENV:", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))  # Debug

client = translate.Client()


def translate_text(text, src, target):
    print("🌐 Translating", text, "from", src, "to", target)  # ✅ Now inside the function
    result = client.translate(text, source_language=src, target_language=target)
    return result["translatedText"]

def detect_language(text):
    result = client.detect_language(text)
    return result["language"]