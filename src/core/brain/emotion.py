"""
CHITT Emotion Engine
"""

class Emotion:

    def __init__(self):

        self.current_emotion = "neutral"

        self.confidence = 1.0

    # ==========================================
    # Detect Emotion
    # ==========================================

    def detect(self, text):

        text = text.lower()

        if any(word in text for word in [
            "happy",
            "great",
            "awesome",
            "good",
            "excellent"
        ]):

            self.current_emotion = "happy"

        elif any(word in text for word in [
            "sad",
            "depressed",
            "cry",
            "hurt"
        ]):

            self.current_emotion = "sad"

        elif any(word in text for word in [
            "angry",
            "mad",
            "hate",
            "annoyed"
        ]):

            self.current_emotion = "angry"

        elif any(word in text for word in [
            "wow",
            "amazing",
            "surprised"
        ]):

            self.current_emotion = "surprised"

        else:

            self.current_emotion = "neutral"

        return self.current_emotion

    # ==========================================
    # Get Emotion
    # ==========================================

    def get(self):

        return self.current_emotion

    # ==========================================
    # Reset
    # ==========================================

    def reset(self):

        self.current_emotion = "neutral"


if __name__ == "__main__":

    emotion = Emotion()

    print(emotion.detect("I am very happy today"))

    print(emotion.get())

"""
=========================================
CHITT - Emotion Manager
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""


class EmotionManager:

    def __init__(self):

        self.current_emotion = "Neutral"

        self.emotion_keywords = {

            "Happy": [
                "happy",
                "great",
                "awesome",
                "nice",
                "good",
                "excellent"
            ],

            "Sad": [
                "sad",
                "upset",
                "bad",
                "cry",
                "depressed"
            ],

            "Angry": [
                "angry",
                "mad",
                "hate",
                "annoying",
                "stupid"
            ],

            "Excited": [
                "wow",
                "amazing",
                "fantastic",
                "super",
                "cool"
            ],

            "Friendly": [
                "hello",
                "hi",
                "thanks",
                "thank you"
            ]

        }

    # ---------------------------------
    # Detect Emotion
    # ---------------------------------

    def detect(self, text):

        text = text.lower()

        for emotion, keywords in self.emotion_keywords.items():

            for keyword in keywords:

                if keyword in text:

                    self.current_emotion = emotion

                    return emotion

        self.current_emotion = "Neutral"

        return "Neutral"

    # ---------------------------------
    # Current Emotion
    # ---------------------------------

    def current(self):

        return self.current_emotion

    # ---------------------------------
    # Set Emotion
    # ---------------------------------

    def set(self, emotion):

        self.current_emotion = emotion

    # ---------------------------------
    # Reset Emotion
    # ---------------------------------

    def reset(self):

        self.current_emotion = "Neutral"

    # ---------------------------------
    # Emotion Response
    # ---------------------------------

    def response_style(self):

        styles = {

            "Happy": "😊 Happy",

            "Sad": "😔 Calm",

            "Angry": "😐 Professional",

            "Excited": "🤩 Energetic",

            "Friendly": "🙂 Friendly",

            "Neutral": "🤖 Neutral"

        }

        return styles.get(

            self.current_emotion,

            "🤖 Neutral"

        )

    # ---------------------------------
    # Show Emotion
    # ---------------------------------

    def show(self):

        print("Current Emotion :", self.current())

        print("Response Style  :", self.response_style())


if __name__ == "__main__":

    emotion = EmotionManager()

    emotion.detect("Hello CHITT")

    emotion.show()

    emotion.detect("Wow this is amazing")

    emotion.show()

    
