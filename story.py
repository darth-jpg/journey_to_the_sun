class Dialogue:
    def __init__(self):
        self.current_dialogue = 0
        self.dialogues = [
            {
                "speaker": "Ricardo",
                "text": "Raquel, the world has been covered in darkness. You must find the sun!",
                "trigger": "start"
            },
            {
                "speaker": "Ricardo",
                "text": "Be careful! The path ahead is full of challenges.",
                "trigger": "first_obstacle"
            },
            {
                "speaker": "Ricardo",
                "text": "Collect these light orbs to illuminate your path!",
                "trigger": "first_collectible"
            },
            {
                "speaker": "Ricardo",
                "text": "You're getting closer to the sun! Keep going!",
                "trigger": "mid_game"
            },
            {
                "speaker": "Ricardo",
                "text": "You've found the sun! The world is saved!",
                "trigger": "end_game"
            },
            {
                "speaker": "Raquel",
                "text": "Ricardo, thank you for guiding me through this journey. Will you be my boyfriend?",
                "trigger": "final_dialogue"
            }
        ]

    def get_dialogue(self, trigger):
        for dialogue in self.dialogues:
            if dialogue["trigger"] == trigger:
                return dialogue
        return None

class StoryProgress:
    def __init__(self):
        self.collectibles_found = 0
        self.total_collectibles = 5
        self.current_level = 1
        self.total_levels = 3
        self.game_completed = False

    def update_progress(self, collectible_found=False, level_completed=False):
        if collectible_found:
            self.collectibles_found += 1
        if level_completed:
            self.current_level += 1
        if self.current_level > self.total_levels:
            self.game_completed = True 