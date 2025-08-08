import json

class DialogueManager:
    def __init__(self):
        self.dialogues = {}

    def load_dialogues(self, path):
        with open(path, encoding='utf-8') as f:
            self.dialogues = json.load(f)

    def get_dialogue(self, npc_id):
        return self.dialogues.get(npc_id, [])
