from data.mission_story import MISSION_STORY

class MissionSystem:
    def __init__(self, act='act2', chapter_idx=0):
        self.act = act
        self.chapter_idx = chapter_idx
        self.story = MISSION_STORY[act]['chapters'][chapter_idx]
        self.dialogue = self.story.get('dialogue', {})
        self.events = self.story['events']
        self.turning_point = MISSION_STORY[act].get('turning_point', '')

    def show_intro(self):
        # Muestra el texto previo al calabozo
        print(f"[INTRO] {self.story['title']}")
        for event in self.events:
            print(f"- {event}")

    def show_dialogue(self, npc_name):
        # Muestra el diálogo con el NPC si existe
        npc_dialogue = self.dialogue.get(npc_name)
        if npc_dialogue:
            print(f"[DIALOGO] {npc_name}:")
            for k, v in npc_dialogue.items():
                if k == 'options':
                    print("Opciones:")
                    for opt in v:
                        print(f"  - {opt['text']}")
                else:
                    print(v)
        else:
            print(f"No hay diálogo definido para {npc_name}.")

    def show_outro(self):
        # Muestra el texto al final de la misión
        print(f"[FIN DE MISION] {self.turning_point}")
