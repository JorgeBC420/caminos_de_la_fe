from ursina import *

class FragmentShopUI(Entity):
    def __init__(self, player, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.player = player
        self.panel = Entity(parent=self, model='quad', scale=(0.8, 0.7), color=color.gold.tint(-0.2))
        Text(parent=self.panel, text='Tienda de Fragmentos', y=0.3, scale=1.5)
        self.fragment_text = Text(parent=self.panel, text=self.get_fragment_text(), y=0.2)
    def get_fragment_text(self):
        fragments = getattr(self.player, 'fragments', {})
        if not fragments:
            return 'Fragmentos: 0'
        return 'Fragmentos: ' + ', '.join([f"{k}: {v}" for k, v in fragments.items()])
        self.unique_items = [
            'Cáliz de la Salvación Eterna',
            'Espejo de las Mil Lunas',
            'Máscara del Dios Sin Rostro',
            'Espada del Juicio Final',
            'Cimitarra de los Cuatro Vientos',
            'Guadaña del Olvido'
        ]
        self.buttons = []
        for i, item in enumerate(self.unique_items):
            btn = Button(parent=self.panel, text=f'Comprar {item} (7 fragmentos)', y=0.1-i*0.13, on_click=lambda it=item: self.buy_item(it))
            self.buttons.append(btn)
        Button(parent=self.panel, text='Cerrar', y=-0.35, color=color.red, on_click=self.close)

    def buy_item(self, item):
        # Determina el tipo de fragmento requerido por el ítem
        fragment_map = {
            'Cáliz de la Salvación Eterna': 'Fragmento del Cáliz',
            'Espejo de las Mil Lunas': 'Fragmento del Espejo',
            'Máscara del Dios Sin Rostro': 'Fragmento de la Máscara',
            'Espada del Juicio Final': 'Fragmento de la Espada',
            'Cimitarra de los Cuatro Vientos': 'Fragmento de la Cimitarra',
            'Guadaña del Olvido': 'Fragmento de la Guadaña'
        }
        fragment_type = fragment_map.get(item)
        fragments = getattr(self.player, 'fragments', {})
        if fragment_type and fragments.get(fragment_type, 0) >= 7:
            fragments[fragment_type] -= 7
            self.fragment_text.text = self.get_fragment_text()
            print(f'¡Has comprado {item}!')
            # Aquí puedes añadir el ítem al inventario del jugador
        else:
            print(f'No tienes suficientes fragmentos de tipo {fragment_type}.')

    def close(self):
        destroy(self)
