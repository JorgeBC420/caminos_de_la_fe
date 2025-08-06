from ursina import *

class ChatUI(Entity):
    def __init__(self, manager, channel='global', **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.manager = manager
        self.channel = channel
        self.panel = Entity(parent=self, model='quad', scale=(0.7, 0.5), color=color.gray)
        self.input = InputField(parent=self.panel, y=-0.2)
        Button(parent=self.panel, text="Enviar", y=-0.3, on_click=self.send_message)
        self.messages_panel = Entity(parent=self.panel)
        self.refresh_messages()
    def send_message(self):
        msg = self.input.text
        self.manager.send_message(self.channel, msg)
        self.input.text = ''
        self.refresh_messages()
    def refresh_messages(self):
        destroy(self.messages_panel)
        self.messages_panel = Entity(parent=self.panel)
        messages = self.manager.fetch_messages(self.channel)
        for i, m in enumerate(messages[-10:]):
            Text(parent=self.messages_panel, text=f"{m['player']}: {m['message']}", y=0.2-i*0.05, x=-0.3)
