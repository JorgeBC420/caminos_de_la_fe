from ursina import *

class DialogueUI(Entity):
    def __init__(self, dialogue_lines, on_close=None, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.dialogue_lines = dialogue_lines
        self.on_close = on_close
        self.current = 0
        self.panel = Entity(parent=self, model='quad', scale=(0.7,0.3), color=color.black66)
        self.text = Text(parent=self.panel, text=self.dialogue_lines[self.current]['text'], y=0.05, scale=1.5)
        self.next_btn = Button(parent=self.panel, text='Siguiente', y=-0.1, on_click=self.next_line)
    def next_line(self):
        self.current += 1
        if self.current < len(self.dialogue_lines):
            self.text.text = self.dialogue_lines[self.current]['text']
        else:
            if self.on_close:
                self.on_close()
            destroy(self)
