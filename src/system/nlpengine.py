class NLPEngine:

    def __init__(self):
        pass

    def process(self, text):

        text = text.lower().strip()

        if any(word in text for word in ["hello", "hi", "hey"]):
            return ("hello", None)

        if "my name is" in text:
            name = text.split("my name is", 1)[1].strip()
            return ("save_name", name)

        if "show memory" in text:
            return ("show_memory", None)

        if "plugins" in text:
            return ("plugins", None)

        return ("unknown", text)
    
