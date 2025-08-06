from ursina import *

class ChestRewardUI(Entity):
    def __init__(self, reward, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.reward = reward
        self.create_ui()

    def create_ui(self):
        Entity(parent=self, model='quad', scale=(0.5, 0.3), color=color.brown)
        Text(parent=self, text=f"¡Has abierto un cofre!", y=0.1, scale=2)
        Text(parent=self, text=f"Recompensa: {self.reward}", y=-0.05, scale=1.5)
        Button(parent=self, text='Cerrar', y=-0.15, scale=(0.2, 0.1), on_click=self.close)

    def close(self):
        destroy(self)

# Simulación de anuncio
class AdRewardUI(Entity):
    def __init__(self, on_reward, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.on_reward = on_reward
        self.create_ui()

    def create_ui(self):
        Entity(parent=self, model='quad', scale=(0.5, 0.3), color=color.azure)
        Text(parent=self, text="Ver anuncio para obtener recompensa", y=0.1, scale=1.5)
        Button(parent=self, text='Ver Anuncio', y=-0.05, scale=(0.2, 0.1), on_click=self.give_reward)
        Button(parent=self, text='Cerrar', y=-0.15, scale=(0.2, 0.1), on_click=self.close)

    def give_reward(self):
        self.on_reward("Llave de Cofre")
        self.close()

    def close(self):
        destroy(self)
