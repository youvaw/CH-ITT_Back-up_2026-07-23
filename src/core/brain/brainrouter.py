# voice/brain_router.py

import datetime
import psutil


class BrainRouter:

    def __init__(self):
        pass

    def process_command(self, text: str) -> str:
        """Analyzes incoming speech text and returns an appropriate response."""
        if not text:
            return "मला काही ऐकू आले नाही."

        clean_text = text.lower().strip()

        # 1. Greetings
        if any(
            word in clean_text
            for word in ["नमस्कार", "हॅलो", "hello", "hi", "नमस्ते"]
        ):
            return "नमस्कार! मी CHITT आहे. मी तुम्हाला कशी मदत करू शकेन?"

        # 2. Time Check
        elif any(
            word in clean_text for word in ["वेळ", "time", "किती वाजले", "time क्या हुआ"]
        ):
            now = datetime.datetime.now().strftime("%I:%M %p")
            return f"सध्या वेळ {now} झाली आहे."

        # 3. System Status Check (CPU / Battery)
        elif any(
            word in clean_text
            for word in ["status", "system", "बॅटरी", "सीपीयूस", "battery"]
        ):
            cpu_usage = psutil.cpu_percent(interval=0.5)
            battery = psutil.sensors_battery()
            percent = battery.percent if battery else "अज्ञात"
            return f"सिस्टम स्थिती: CPU वापर {cpu_usage} टक्के आहे, आणि बॅटरी {percent} टक्के आहे."

        # 4. Identity Questions
        elif any(
            word in clean_text
            for word in ["कोण आहेस", "तुमचं नाव काय", "who are you"]
        ):
            return (
                "मी CHITT आहे, तुमचा पर्सनल AI व्हॉईस असिस्टंट."
            )

        # 5. Fallback Response
        else:
            return f"मला समझले: '{text}'. पण यावर कोणती एक्शन घ्यायची हे अजून सेट नाही केले आहे."


if __name__ == "__main__":
    router = BrainRouter()
    print("Test 1:", router.process_command("हॅलो"))
    print("Test 2:", router.process_command("वेळ काय झाली आहे"))
    
