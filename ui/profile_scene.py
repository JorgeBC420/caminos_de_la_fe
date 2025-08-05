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
from ui.level_up_ui import LevelUpUI
from ui.inventory_ui import InventoryUI


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
        # Panel de nivel y XP (centralizado)
        self.level_panel = Text(f"{self.lang.t('level')}: {self.player.level}", position=(0.1,0.45), scale=1.5, color=color.gold)
        self.xp_panel = Text(f"XP: {self.player.experience}/{self.player.experience_to_next_level}", position=(0.1,0.42), scale=1, color=color.yellow)
        # Panel de stats (centralizado)
        stats = self.player.stats.max_health, getattr(self.player.stats, 'attack_power', 10)
        self.stats_panel = Text(f"{self.lang.t('stats')}: HP {stats[0]}, ATK {stats[1]}", position=(0.1,0.4))
        self.faction_panel = Text(f"{self.lang.t('faction')}: {self.player.faction}", position=(0.1,0.3))
        self.equipment_panel = Text(f"{self.lang.t('equipment')}: {self.player.equipment}", position=(0.1,0.2))
        self.change_faction_btn = Button(text=self.lang.t('change_faction'), position=(0.1,0.1), on_click=self.change_faction)
        self.rotate_btn = Button(text=self.lang.t('rotate_character'), position=(0.1,0.0), on_click=self.toggle_rotation, highlight_color=color.azure)
        # Feedback visual para botones
        for btn in [self.change_faction_btn, self.rotate_btn, self.level_up_btn, self.inventory_btn, self.dungeon_btn]:
            btn.highlight_color = color.azure
        self.level_up_btn = Button(text=self.lang.t('level_up'), position=(0.1,-0.1), color=color.green, on_click=self.open_level_up)
        self.inventory_btn = Button(text=self.lang.t('inventory_tab'), position=(0.3,0.1), color=color.azure, on_click=self.open_inventory)
        # Botón para misiones/mapa/calabozo
        self.dungeon_btn = Button(text=self.lang.t('dungeon_tab') if hasattr(self.lang, 't') and self.lang.t('dungeon_tab') else 'Misiones', position=(0.3,0.0), color=color.orange, on_click=self.open_mission_map)
        self.tabs = [
            (self.lang.t('profile_tab'), self.show_stats),
            (self.lang.t('equipment_tab'), self.show_equipment),
            (self.lang.t('inventory_tab'), self.show_inventory),
            (self.lang.t('skills_tab'), self.show_skills),
            (self.lang.t('brotherhood_tab'), self.show_brotherhood)
        ]
        self.tab_buttons = []
        for i, (tab_name, tab_func) in enumerate(self.tabs):
            btn = Button(text=tab_name, position=(0.5,0.4-i*0.08), scale=(0.18,0.06), color=color.gray, on_click=tab_func)
            self.tab_buttons.append(btn)

    def open_mission_map(self):
        # Abre pantalla de selección de calabozo/misión
        if self.profile_scene:
            self.profile_scene.show_dungeon_selection()
            print('Pantalla de selección de calabozo abierta.')

    def show_stats(self):
        self.stats_panel.enabled = True
        self.level_panel.enabled = True
        self.xp_panel.enabled = True
        self.equipment_panel.enabled = False
        # ...otros paneles ocultos...

    def show_equipment(self):
        self.stats_panel.enabled = False
        self.level_panel.enabled = False
        self.xp_panel.enabled = False
        self.equipment_panel.enabled = True
        # ...otros paneles ocultos...

    def show_inventory(self):
        self.open_inventory()

    def show_skills(self):
        # Panel de habilidades: muestra skills y permite activarlas
        from ursina import Text, Button, color, camera
        # Limpia panel anterior si existe
        if hasattr(self, 'skills_panel'):
            self.skills_panel.enabled = False
            destroy(self.skills_panel)
        self.skills_panel = Entity(parent=camera.ui, model='quad', color=color.rgba(30,30,60,180), scale=(0.6,0.5), position=(0.2,0,2))
        # Obtiene skills del jugador (incluye skills de facción/deidad)
        skills = []
        # Skills base del jugador
        if hasattr(self.player, 'skills'):
            skills.extend(self.player.skills)
        # Skills de facción/deidad
        if hasattr(self.player, 'faction') and hasattr(self.player, 'deity'):
            from data.deity_data import DEITY_BONUSES
            deity_skills = DEITY_BONUSES.get(self.player.deity, {}).get('skills', [])
            skills.extend(deity_skills)
        # Si no hay skills, muestra mensaje
        if not skills:
            Text('No tienes habilidades desbloqueadas.', parent=self.skills_panel, position=(0,0.2), scale=1.2, color=color.red)
            return
        # Muestra cada skill con botón de activación y cooldown
        self.skill_buttons = []
        y_start = 0.18
        for i, skill in enumerate(skills):
            skill_name = skill.get('name', skill) if isinstance(skill, dict) else str(skill)
            skill_desc = skill.get('desc', '') if isinstance(skill, dict) else ''
            cooldown = skill.get('cooldown', 0) if isinstance(skill, dict) else 0
            def activate_skill(skill=skill):
                # Lógica de activación: llama a método en player_skills
                from skills.player_skills import PlayerSkills
                ps = PlayerSkills(self.player)
                result = ps.use_special(skill_name)
                print(f'Habilidad activada: {skill_name} - {result}')
                # Feedback visual
                self.skills_panel.color = color.rgba(60,180,60,200)
                import threading
                threading.Timer(0.5, lambda: setattr(self.skills_panel, 'color', color.rgba(30,30,60,180))).start()
            btn = Button(text=f'{skill_name}', parent=self.skills_panel, scale=(0.5,0.09), position=(0, y_start-i*0.13), color=color.azure, on_click=activate_skill)
            self.skill_buttons.append(btn)
            # Descripción y cooldown
            Text(skill_desc, parent=self.skills_panel, position=(0.25, y_start-i*0.13), scale=0.8, color=color.white)
            if cooldown:
                Text(f'CD: {cooldown}s', parent=self.skills_panel, position=(-0.25, y_start-i*0.13), scale=0.8, color=color.yellow)
        # Botón para cerrar panel
        Button(text='Cerrar', parent=self.skills_panel, scale=(0.2,0.08), position=(0,-0.35), color=color.red, on_click=lambda: destroy(self.skills_panel))

    def show_brotherhood(self):
        print('Mostrar panel de hermandad (pendiente)')
    def open_level_up(self):
        # Solo permite si hay skill points disponibles
        if getattr(self.player, 'skill_points', 0) > 0:
            LevelUpUI(self.player, on_confirm=self.update_stats)
        else:
            print('No tienes puntos de habilidad disponibles.')

    def open_inventory(self):
        InventoryUI(self.player, on_equip=self.equip_item)

    def equip_item(self, item):
        # Lógica básica de equipar: reemplaza el equipo y actualiza la UI
        slot = getattr(item, 'slot', None)
        if slot:
            old_item = self.player.equipment.get(slot)
            if old_item:
                self.player.inventory.append(old_item)
            self.player.equipment[slot] = item
            self.player.inventory.remove(item)
            self.update_equipment()
            print(f'Equipado: {item.name} en {slot}')

    def update_stats(self):
        stats = self.player.stats.max_health, getattr(self.player.stats, 'attack_power', 10)
        self.stats_panel.text = f"{self.lang.t('stats')}: HP {stats[0]}, ATK {stats[1]}"
        self.level_panel.text = f"{self.lang.t('level')}: {self.player.level}"
        self.xp_panel.text = f"XP: {self.player.experience}/{self.player.experience_to_next_level}"
        print('Stats y nivel actualizados:', stats)

    def update_equipment(self):
        self.equipment_panel.text = f"{self.lang.t('equipment')}: {self.player.equipment}"
        print('Equipo actualizado:', self.player.equipment)

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

    def toggle_rotation(self):
        # Alterna rotación automática del personaje
        if self.profile_scene and hasattr(self.profile_scene, 'toggle_player_rotation'):
            self.profile_scene.toggle_player_rotation()
    def go_quests(self):
        # Integrar con barra inferior
        self.open_mission_map()

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
    def toggle_player_rotation(self):
        # Unifica lógica de rotación automática/manual
        if not hasattr(self, 'rotation_enabled'):
            self.rotation_enabled = True
        self.rotation_enabled = not self.rotation_enabled
        if self.rotation_enabled:
            if hasattr(self, 'player_model'):
                self.player_model.animate_rotation_y(self.player_model.rotation_y+360, duration=10, loop=True)
        else:
            if hasattr(self, 'player_model'):
                self.player_model.stop()
    def show_dungeon_selection(self):
        # Pantalla simple para seleccionar calabozo y mostrar historia
        from ursina import Entity, Text, Button, camera, color, destroy
        import random
        self.dungeon_menu_bg = Entity(parent=camera.ui, model='quad', color=color.rgba(20,20,20,220), scale=(0.7,0.7), position=(0,0,2))
        # Ejemplo de calabozos genéricos
        dungeons = [
            {'name': 'Catacumbas Oscuras', 'story': 'Un antiguo lugar lleno de secretos y peligros.'},
            {'name': 'Ruinas Perdidas', 'story': 'Explora las ruinas y descubre su historia olvidada.'},
            {'name': 'Cueva del Eco', 'story': 'Una cueva misteriosa donde el eco revela pistas.'},
            {'name': 'Fortaleza Abandonada', 'story': 'Enfrenta a los guardianes de la fortaleza.'},
            {'name': 'Bosque Maldito', 'story': 'Un bosque donde la oscuridad reina.'}
        ]
        y_start = 0.2
        self.dungeon_buttons = []
        for i, dungeon in enumerate(dungeons):
            def select_dungeon(dungeon=dungeon):
                # Muestra historia antes de entrar
                for b in self.dungeon_buttons:
                    destroy(b)
                self.dungeon_story_text = Text(f"{dungeon['name']}\n\n{dungeon['story']}", parent=self.dungeon_menu_bg, position=(0,0.15), scale=1.2, color=color.white)
                self.enter_dungeon_btn = Button(text='Entrar', parent=self.dungeon_menu_bg, position=(0,-0.2), scale=(0.2,0.08), color=color.orange,
                    on_click=lambda: self.enter_selected_dungeon(dungeon))
            btn = Button(text=dungeon['name'], parent=self.dungeon_menu_bg, scale=(0.5,0.09), position=(0, y_start-i*0.13), color=color.gray, on_click=select_dungeon)
            self.dungeon_buttons.append(btn)

    def enter_selected_dungeon(self, dungeon):
        # Destruye menú y genera calabozo
        from ursina import destroy
        if hasattr(self, 'dungeon_menu_bg'):
            destroy(self.dungeon_menu_bg)
        if hasattr(self, 'dungeon_story_text'):
            destroy(self.dungeon_story_text)
        if hasattr(self, 'enter_dungeon_btn'):
            destroy(self.enter_dungeon_btn)
        self.generate_random_dungeon()
        print(f"Entrando a: {dungeon['name']}")
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
        # Adaptación móvil
        if platform.system() == 'Android':
            self.bg.scale = (2,1.5,1)
            for btn in self.profile_ui.tab_buttons+[self.profile_ui.dungeon_btn]:
                btn.scale = (0.3,0.12)
            print('Modo móvil: UI ajustada')
        self.home = None
        self.load_home_async(getattr(player, 'home_level', 1))
        # Persistencia global: carga datos al entrar
        if hasattr(player, 'load_data'):
            player.load_data()
        # Instancia enemigos y objetos de prueba al azar
        self.spawn_random_entities(player)

    def spawn_random_entities(self, player):
        import random
        # Oleadas de enemigos: entre 1 y 3 oleadas, cada una con 5-40 enemigos
        num_waves = random.randint(1, 3)
        for wave in range(num_waves):
            num_enemies = random.randint(5, 40)
            for _ in range(num_enemies):
                x, y, z = random.uniform(-8,8), 0.5, random.uniform(-8,8)
                enemy = None
                if hasattr(player, 'create_test_enemy'):
                    enemy = player.create_test_enemy(position=(x, y, z))
                if enemy:
                    enemy.enabled = True
        # Objetos: entre 5 y 15 por mapa
        num_objects = random.randint(5, 15)
        for _ in range(num_objects):
            x, y, z = random.uniform(-8,8), 0.5, random.uniform(-8,8)
            obj = None
            if hasattr(player, 'create_test_object'):
                obj = player.create_test_object(position=(x, y, z))
            if obj:
                obj.enabled = True

    def generate_random_dungeon(self):
        # Genera un mapa aleatorio estilo calabozo usando modelos Ursina
        # Ejemplo simple: crea habitaciones y pasillos con cubos
        from ursina import Entity
        import random
        num_rooms = random.randint(3, 8)
        for i in range(num_rooms):
            x, z = random.uniform(-12,12), random.uniform(-12,12)
            room = Entity(model='cube', color=color.gray, position=(x,0,z), scale=(random.uniform(3,6),1,random.uniform(3,6)), texture='brick')
        # Pasillos (opcional): conectar habitaciones
        # Puedes expandir esto con modelos personalizados, puertas, trampas, etc.

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
        # Persistencia global: guarda datos al salir
        if hasattr(self.profile_ui.player, 'save_data'):
            self.profile_ui.player.save_data()
        # Animación de salida y limpieza de entidades
        self.bg.animate_scale((0,0,0), duration=0.3, curve=curve.in_expo)
        destroy(self.profile_ui)
        destroy(self.bg)
        if hasattr(self, 'player_model'):
            destroy(self.player_model)
        if hasattr(self, 'home'):
            destroy(self.home)
        if hasattr(self, 'effect_pool'):
            del self.effect_pool
        if hasattr(self, 'dungeon_menu_bg'):
            destroy(self.dungeon_menu_bg)
        if hasattr(self, 'dungeon_story_text'):
            destroy(self.dungeon_story_text)
        if hasattr(self, 'enter_dungeon_btn'):
            destroy(self.enter_dungeon_btn)
        import gc; gc.collect()
        super().destroy()
