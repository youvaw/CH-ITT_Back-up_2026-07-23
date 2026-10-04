"""
CHITT AI
Learning Engine
"""


class LearningEngine:
    """
    Learns from conversations and stores knowledge.
    """

    def __init__(self):
        self.knowledge = {}

    def learn(self, key: str, value: str):

        self.knowledge[key] = value

    def recall(self, key: str):

        return self.knowledge.get(key, None)

    def forget(self, key: str):

        if key in self.knowledge:
            del self.knowledge[key]

    def clear(self):

        self.knowledge.clear()
"""
CHITT Learning Engine
Learns from conversations and experiences.
"""

import json
from pathlib import Path


class LearningEngine:

    def __init__(self):

        self.learning_path = Path("data/learning")

        self.learning_path.mkdir(parents=True, exist_ok=True)

        self.learning_file = self.learning_path / "learning.json"

        self.knowledge = []

        self.load()

    # ==========================================
    # Load Learning Data
    # ==========================================

    def load(self):

        if self.learning_file.exists():

            try:

                with open(
                    self.learning_file,
                    "r",
                    encoding="utf-8"
                ) as file:

                    self.knowledge = json.load(file)

            except Exception:

                self.knowledge = []

        else:

            self.knowledge = []

    # ==========================================
    # Save Learning Data
    # ==========================================

    def save(self):

        with open(
            self.learning_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.knowledge,
                file,
                indent=4,
                ensure_ascii=False
            )

    # ==========================================
    # Learn New Information
    # ==========================================

    def learn(self, user_input, response):

        lesson = {

            "user": user_input,

            "response": response

        }

        self.knowledge.append(lesson)

        self.save()

    # ==========================================
    # Search Learned Knowledge
    # ==========================================

    def search(self, keyword):

        keyword = keyword.lower()

        results = []

        for item in self.knowledge:

            if (

                keyword in item["user"].lower()

                or

                keyword in item["response"].lower()

            ):

                results.append(item)

        return results

    # ==========================================
    # Get All Knowledge
    # ==========================================

    def get_all(self):

        return self.knowledge

    # ==========================================
    # Clear Knowledge
    # ==========================================

    def clear(self):

        self.knowledge = []

        self.save()

    # ==========================================
    # Total Learned Items
    # ==========================================

    def total(self):

        return len(self.knowledge)


if __name__ == "__main__":

    engine = LearningEngine()

    engine.learn(

        "Hello",

        "Hello Avishkar"

    )

    print(engine.search("hello"))

    print("Total Learned :", engine.total())
            
