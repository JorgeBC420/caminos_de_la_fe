from ursina import *

class RewardsUI(Entity):
    def __init__(self, rewards_data, on_continue_callback, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.on_continue = on_continue_callback
        Button(parent=self, model='quad', scale=99, color=color.black66)
        panel = Entity(parent=self, model='quad', scale=(0.8, 0.6), texture='assets/ui/panel_texture.png')
        Text(parent=panel, text="¡Misión Completada!", y=0.4, scale=2, color=color.gold)
        y_pos = 0.2
        if 'xp' in rewards_data:
            Text(parent=panel, text=f"+ {rewards_data['xp']} XP", y=y_pos)
            y_pos -= 0.1
        if 'gold' in rewards_data:
            Text(parent=panel, text=f"+ {rewards_data['gold']} ORO", y=y_pos)
            y_pos -= 0.1
        if rewards_data.get('items'):
            for item_id in rewards_data['items']:
                Text(parent=panel, text=f"Obtenido: {item_id}", y=y_pos)
                y_pos -= 0.1
        Button(parent=panel, text="Continuar", y=-0.4, on_click=self.close)
    def close(self):
        self.on_continue()
        destroy(self)
