from ursina import *
from systems.event_system import EventSystem

class EventEndUI(Entity):
    def __init__(self, player, event_name, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.player = player
        self.event_name = event_name
        self.msg_text = Text(text='', y=0.3, color=color.white)
        Button(text='Convertir monedas de evento en oro', y=0.1, color=color.azure, on_click=self.convert)
        Button(text='Cerrar', y=-0.1, color=color.gray, on_click=self.close)

    def convert(self):
        event_system = EventSystem()
        event_system.end_event(self.event_name, self.player, ui=self)
        # El mensaje se mostrará en self.message

    @property
    def message(self):
        return self.msg_text.text

    @message.setter
    def message(self, value):
        self.msg_text.text = value

    def close(self):
        destroy(self)
