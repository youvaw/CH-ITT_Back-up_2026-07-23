from .voice_manager import VoiceManager


def main():

    voice = VoiceManager()

    voice.speak("नमस्कार. मी CHITT आहे. मला काहीतरी बोला.")

    text = voice.listen()

    if text:
        voice.speak(f"तुम्ही म्हणालात: {text}")
    else:
        voice.speak("मला तुमचा आवाज समजला नाही.")


if __name__ == "__main__":
    main()
    