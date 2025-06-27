from google.cloud import texttospeech

"""def synthesize_speech(text, language_code="en-IN"):
    
    Converts text into speech using Google Cloud TTS with Indian-accented voices.

    :param text: The response text to convert into speech.
    :param language_code: Language code like "en-IN", "hi-IN", "en-US"
    :return: MP3 audio content in bytes
    
    client = texttospeech.TextToSpeechClient()

    # Preferred voices with natural Indian accents
    preferred_voices = {
        "en-IN": "en-IN-Wavenet-C",   # Indian English (Female)
        "en-US": "en-IN-Wavenet-A",   # fallback to Indian English for US input
        "hi-IN": "hi-IN-Wavenet-A",   # Hindi (Female)
        "mr-IN": "mr-IN-Wavenet-A",   # Marathi
        "bn-IN": "bn-IN-Wavenet-A",   # Bengali
        "ta-IN": "ta-IN-Wavenet-A",   # Tamil
        "te-IN": "te-IN-Wavenet-A",   # Telugu
        "gu-IN": "gu-IN-Wavenet-A",   # Gujarati
        "ml-IN": "ml-IN-Wavenet-A",   # Malayalam
        "kn-IN": "kn-IN-Wavenet-A",   # Kannada
        "pa-IN": "pa-IN-Wavenet-A",   # Punjabi

    }

    # Fallback if the requested language is not supported
    selected_language = language_code if language_code in preferred_voices else "en-IN"
    selected_voice = preferred_voices[selected_language]

    # Voice configuration
    voice = texttospeech.VoiceSelectionParams(
        language_code=selected_language,
        name=selected_voice,
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    # Output format
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=1.07,               # Slightly slower = more human
        pitch=-1.0,                       # Slightly lower pitch = warmer tone
        volume_gain_db=2.0,              # Slight boost in volume
        effects_profile_id=["telephony-class-application"],  # Optimize for phone call clarity
    )

    # Synthesize
    synthesis_input = texttospeech.SynthesisInput(text=text)
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
    )

    return response.audio_content"""


from google.cloud import texttospeech

def synthesize_speech(text, language_code="en-IN", voice_name=None):
    """
    Converts text into speech using Google Cloud TTS with Indian-accented voices.

    :param text: The response text to convert into speech.
    :param language_code: Language code like "en-IN", "hi-IN", "en-US"
    :param voice_name: Optional specific voice to use (e.g., "en-IN-Wavenet-C")
    :return: MP3 audio content in bytes
    """
    client = texttospeech.TextToSpeechClient()

    # Preferred voices with natural Indian accents
    preferred_voices = {
        "en-IN": "en-IN-Wavenet-A",   # Indian English (Female)
        "en-US": "en-IN-Wavenet-A",   # fallback to Indian English
        "hi-IN": "hi-IN-Wavenet-A",
        "mr-IN": "mr-IN-Wavenet-A",
        "bn-IN": "bn-IN-Wavenet-A",
        "ta-IN": "ta-IN-Wavenet-A",
        "te-IN": "te-IN-Wavenet-A",
        "gu-IN": "gu-IN-Wavenet-A",
        "ml-IN": "ml-IN-Wavenet-A",
        "kn-IN": "kn-IN-Wavenet-A",
        "pa-IN": "pa-IN-Wavenet-A",
    }

    # 🔧 Allow explicit voice override
    if voice_name:
        selected_voice = voice_name
        selected_language = language_code
    else:
        selected_language = language_code if language_code in preferred_voices else "en-IN"
        selected_voice = preferred_voices[selected_language]

    # Voice configuration
    voice = texttospeech.VoiceSelectionParams(
        language_code=selected_language,
        name=selected_voice,
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    # Output config
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=1.07,
        pitch=-1.0,
        volume_gain_db=2.0,
        effects_profile_id=["telephony-class-application"],
    )

    # Synthesize speech
    synthesis_input = texttospeech.SynthesisInput(text=text)
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
    )

    return response.audio_content
