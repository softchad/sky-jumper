import json
import os

class Achievements:
    def __init__(self):
        self.achievements = {
            "score_100": {"unlocked": False, "description": "Score 100 points", "color": (191, 10, 14)},
            "score_200": {"unlocked": False, "description": "Score 200 points", "color": (65, 197, 9)},
            "score_300": {"unlocked": False, "description": "Score 300 points", "color": (166, 14, 194)},
            "score_400": {"unlocked": False, "description": "Score 400 points", "color": (12, 194, 190)},
            "score_500": {"unlocked": False, "description": "Score 500 points", "color": (191, 93, 10)},
            "score_600": {"unlocked": False, "description": "Score 600 points", "color": (186, 198, 14)},
            "score_700": {"unlocked": False, "description": "Score 700 points", "color": (14, 201, 120)},
            "score_800": {"unlocked": False, "description": "Score 800 points", "color": (198, 56, 14)},
            "score_900": {"unlocked": False, "description": "Score 900 points", "color": (62, 56, 222)},
            "score_1000": {"unlocked": False, "description": "Score 1000 points", "color": (208, 23, 104)},
            "score_1100": {"unlocked": False, "description": "Score 1100 points", "color": (234, 217, 45)},
            "score_1200": {"unlocked": False, "description": "Score 1200 points", "color": (0, 124, 222)},
            "score_1300": {"unlocked": False, "description": "Score 1300 points", "color": (254, 8, 76)},
            "score_1400": {"unlocked": False, "description": "Score 1400 points", "color": (221, 0, 178)},
            "score_1500": {"unlocked": False, "description": "Score 1500 points", "color": (0, 0, 0)},
        }
        self.progress = {"score": 0}
        self.last_unlocked_achievement = None
        self.load_achievements()

    def load_achievements(self):
        if os.path.exists("achievements.json"):
            with open("achievements.json", "r") as f:
                data = json.load(f)
                self.achievements.update(data.get("achievements", {}))
                self.last_unlocked_achievement = data.get("last_unlocked_achievement", None)
        else:
            print("No save file found at achievements.json. Starting with default achievements.")

    def save_achievements(self):
        with open("achievements.json", "w") as f:
            data = {
                "achievements": self.achievements,
                "last_unlocked_achievement": self.last_unlocked_achievement
            }
            json.dump(data, f)

    def check_achievements(self):
        score = self.progress["score"]
        for key in sorted(self.achievements.keys()):
            achievement_score = int(key.split("_")[1])
            if score >= achievement_score and not self.achievements[key]["unlocked"]:
                self.achievements[key]["unlocked"] = True
                self.last_unlocked_achievement = key
                self.save_achievements()

    def get_achievements(self):
        return self.achievements
