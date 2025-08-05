import threading
import platform

# Pooling de entidades
class EntityPool:
    def __init__(self, entity_type, count):
        self.pool = [entity_type(enabled=False) for _ in range(count)]
    def get_entity(self):
        for e in self.pool:
            if not e.enabled:
                e.enabled = True
                return e
        return self.pool[0].clone()

from ursina import Entity, Scene, Text, Button, color, camera, destroy, curve, application
from systems.lang_manager import LanguageManager
from entities.player import Player


import requests

class ProfileUI(Entity):
    def __init__(self, player: Player, lang_manager: LanguageManager, profile_scene=None, **kwargs):
        super().__init__(**kwargs)
        self.player = player
        self.lang = lang_manager
        self.profile_scene = profile_scene
        self.rotation_angle = 0
        self.create_panels()

    def create_panels(self):
        # Panel de stats con localización avanzada
        self.stats_panel = Text(f"{self.lang.t('stats')}: {self.player.stats}", position=(0.1,0.4))
        self.faction_panel = Text(f"{self.lang.t('faction')}: {self.player.faction}", position=(0.1,0.3))
        self.equipment_panel = Text(f"{self.lang.t('equipment')}: {self.player.equipment}", position=(0.1,0.2))
        self.change_faction_btn = Button(text=self.lang.t('change_faction'), position=(0.1,0.1), on_click=self.change_faction)
        self.rotate_btn = Button(text=self.lang.t('rotate_character'), position=(0.1,0.0), on_click=self.rotate_character)
        # Traducción dinámica de pestañas y botones
        self.tabs = [
            (self.lang.t('profile_tab'), self.show_stats),
            (self.lang.t('equipment_tab'), self.show_equipment),
            (self.lang.t('inventory_tab'), self.show_inventory),
            (self.lang.t('skills_tab'), self.show_skills),
            (self.lang.t('brotherhood_tab'), self.show_brotherhood)
        ]
        # Puedes crear los botones de navegación aquí usando self.tabs

    def change_faction(self):
        # Solicita facciones según el nivel del jugador
        try:
            response = requests.get(f'http://localhost:8000/factions/{self.player.level}')
            if response.ok:
                factions = response.json().get('factions', [])
                print(f"Facciones disponibles: {factions}")
                self.show_faction_menu(factions)
        except Exception as e:
            print(f"Error obteniendo facciones: {e}")

    def show_faction_menu(self, factions):
        # Muestra un menú simple para elegir facción con localización
        from ursina import window
        menu_bg = Entity(parent=camera.ui, model='quad', color=color.rgba(0,0,0,180), scale=(0.5,0.5), position=(0,0,2))
        buttons = []
        y_start = 0.15
        for i, fac in enumerate(factions):
            def set_faction(fac=fac):
                advanced = ['vikingos', 'romanos', 'egipcios']
                if fac in advanced and self.player.level < 50:
                    print(self.lang.t('advanced_faction_locked'))
                else:
                    self.player.faction = fac
                    self.faction_panel.text = f"{self.lang.t('faction')}: {self.lang.t(fac)}"
                    print(f"Facción cambiada a: {self.lang.t(fac)}")
                for b in buttons:
                    destroy(b)
                destroy(menu_bg)
            btn = Button(text=self.lang.t(fac), parent=menu_bg, scale=(0.4,0.1), position=(0, y_start-i*0.13), on_click=set_faction)
            buttons.append(btn)

    def rotate_character(self):
        # Permite rotar el modelo del personaje en la escena 3D
        if self.profile_scene and hasattr(self.profile_scene, 'player_model'):
            self.rotation_angle = (self.rotation_angle + 45) % 360
            self.profile_scene.player_model.rotation_y = self.rotation_angle

    def update_profile_data(self):
        # Ejemplo: obtener datos dinámicos del perfil desde FastAPI
        try:
            response = requests.get(f'http://localhost:8000/profile/{self.player.id}')
            if response.ok:
                data = response.json()
                self.stats_panel.text = f"{self.lang.t('stats')}: {data.get('stats', {})}"
                self.faction_panel.text = f"{self.lang.t('faction')}: {data.get('faction', '')}"
        except Exception as e:
            print(f"Error obteniendo perfil: {e}")

class ProfileScene(Scene):
    def __init__(self, player: Player, lang_manager: LanguageManager, **kwargs):
        super().__init__(**kwargs)
        # Verifica conexión a internet
        if not self.check_internet():
            self.bg = Entity(model='quad', color=color.rgba(0,0,0,220), scale=(1.5,1,1), z=-1)
            Text('Conexión a internet requerida para jugar.', parent=self.bg, scale=2, color=color.red, position=(0,0))
            Button(text='Salir', parent=self.bg, scale=(0.3,0.1), position=(0,-0.3), color=color.red, on_click=application.quit)
            print('No hay conexión a internet. Juego bloqueado.')
            return
        self.bg = Entity(model='quad', texture='assets/textures/profile_bg.png', scale=(1.5,1,1), z=-1)
        self.bg.animate_scale((1.5,1,1), duration=0.4, curve=curve.out_expo)
        self.profile_ui = ProfileUI(player, lang_manager, profile_scene=self)
        self.effect_pool = EntityPool(lambda: Entity(model='sphere', color=color.azure, enabled=False), 10)
        if platform.system() == 'Android':
            self.bg.scale = (2,1.5,1)
            print('Modo móvil: UI ajustada')
        self.home = None
        self.load_home_async(getattr(player, 'home_level', 1))

    def check_internet(self):
        import socket
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=2)
            return True
        except OSError:
            return False

    def load_home_async(self, home_level):
        def callback(model_path):
            if self.home:
                destroy(self.home)
            self.home = Entity(model=model_path, position=(10,0,10), scale=3, texture='brick')
        def loader():
            # Simula carga de modelo (puedes usar tu propio loader)
            import time; time.sleep(1)
            callback(f'assets/homes/level_{home_level}.glb')
        threading.Thread(target=loader).start()

    def destroy(self):
        # Animación de salida y limpieza de entidades
        self.bg.animate_scale((0,0,0), duration=0.3, curve=curve.in_expo)
        destroy(self.profile_ui)
        destroy(self.bg)
        super().destroy()
