from data.mission_builds import PRESET_BUILDS
from scenes.build_selection import BuildSelection
from entities.player import Player
from systems.ad_manager import AdManager
from systems.faith_pass import FaithPass
from systems.progression_limits import ProgressionLimits
from ui.deity_selection_ui import DeitySelectionUI

class MissionManager:
    # Protección (escudo) y cooldowns de ataque
    def set_shield(self, player):
        """Otorga escudo de protección por 30 minutos tras atacar o defender."""
        from datetime import datetime, timedelta
        player.shield_until = datetime.now() + timedelta(minutes=30)
        print(f"{getattr(player, 'name', 'Jugador')} tiene escudo de protección hasta {player.shield_until}")

    def can_attack(self, player):
        """Verifica si el jugador puede atacar según cooldown y tipo de cuenta."""
        from datetime import datetime, timedelta
        last_attack = getattr(player, 'last_attack', None)
        is_premium = getattr(player, 'is_premium', False)
        cooldown = timedelta(minutes=5) if is_premium else timedelta(minutes=10)
        if last_attack and datetime.now() < last_attack + cooldown:
            print(f"Debes esperar antes de atacar de nuevo. Cooldown restante: {(last_attack + cooldown - datetime.now()).seconds//60} min")
            return False
        return True

    def register_attack(self, player):
        """Registra el ataque y actualiza el cooldown."""
        from datetime import datetime
        player.last_attack = datetime.now()
        print(f"{getattr(player, 'name', 'Jugador')} ha atacado. Cooldown iniciado.")

    def is_shielded(self, player):
        """Verifica si el jugador tiene escudo activo."""
        from datetime import datetime
        shield_until = getattr(player, 'shield_until', None)
        if shield_until and datetime.now() < shield_until:
            print(f"{getattr(player, 'name', 'Jugador')} está protegido por escudo.")
            return True
        return False

    # Integración con UI de inventario avanzado y sistema de misiones
    def open_advanced_inventory_ui(self):
        print("[UI] Inventario avanzado abierto.")
        # Aquí se llamaría a la UI real

    def trigger_mission_for_unique_item(self, player, item):
        print(f"[MISIÓN] Misión de purificación iniciada para {item}.")
        # Aquí se integraría con el sistema de misiones

    # Anuncios y banners
    def show_popup_ad(self):
        print("[AD] Pop-up mostrado (cada 30 minutos)")

    def show_static_banner(self):
        print("[AD] Banner estático mostrado por 1 minuto (cada 5 minutos)")
    # Duelos 1vs1 con apuesta de ítem
    def start_duel(self, opponent, wager_item=None):
        """Inicia un duelo 1vs1 con apuesta de ítem activada."""
        self.duel_opponent = opponent
        self.duel_wager_item = wager_item
        print(f"Duelo iniciado contra {getattr(opponent, 'name', 'oponente')} por el ítem: {wager_item}")

    def resolve_duel(self, winner, loser):
        """Resuelve el duelo, aplica maldición y transfiere el ítem apostado."""
        # Maldición del Perdedor: -15% stats por 2h
        from datetime import datetime, timedelta
        loser.curse_until = datetime.now() + timedelta(hours=2)
        if not hasattr(loser, 'stat_modifier'):
            loser.stat_modifier = 1.0
        loser.stat_modifier *= 0.85
        print(f"{getattr(loser, 'name', 'Perdedor')} sufre la Maldición del Perdedor (-15% stats por 2h)")
        # El ganador obtiene el ítem pero no puede usarlo hasta purificarlo
        if self.duel_wager_item:
            if not hasattr(winner, 'unique_items'):
                winner.unique_items = []
            winner.unique_items.append(self.duel_wager_item)
            winner.purification_required = True
            winner.purification_mission_until = datetime.now() + timedelta(hours=24)
            print(f"{getattr(winner, 'name', 'Ganador')} obtiene el ítem único '{self.duel_wager_item}' pero debe purificarlo (misión de 24h)")

    def can_use_unique_item(self, player):
        """Solo puede usar el ítem si ha completado la misión de purificación."""
        from datetime import datetime
        if getattr(player, 'purification_required', False):
            if datetime.now() < getattr(player, 'purification_mission_until', datetime.now()):
                print("No puedes usar el ítem único hasta completar la misión de purificación.")
                return False
            else:
                player.purification_required = False
        return True

    def apply_unique_item_risk(self, player):
        """Aplica riesgo: maldición semanal y aura visible si no completa misiones."""
        from datetime import datetime, timedelta
        if not hasattr(player, 'last_weekly_mission'):  # Simulación de control semanal
            player.last_weekly_mission = datetime.now() - timedelta(days=8)
        if (datetime.now() - player.last_weekly_mission).days >= 7:
            player.stat_modifier *= 0.9
            player.has_cursed_aura = True
            print("El ítem único maldice al portador (-10% stats, aura visible)")
        else:
            player.has_cursed_aura = False

    def show_unique_item_aura(self, player):
        """Muestra el aura visual si el jugador tiene ítem único y está maldito."""
        if getattr(player, 'has_cursed_aura', False):
            print(f"{getattr(player, 'name', 'Jugador')} emite un aura visible: ¡riesgo de ser cazado!")

    # Backend hooks (simulados)
    def send_duel_result_to_backend(self, winner, loser, item):
        """Envía el resultado del duelo al backend (simulado)."""
        print(f"[BACKEND] Duelo registrado: {getattr(winner, 'name', 'Ganador')} ganó '{item}' a {getattr(loser, 'name', 'Perdedor')}")

    def update_player_stats_backend(self, player):
        """Actualiza los stats del jugador en el backend (simulado)."""
        print(f"[BACKEND] Stats actualizados para {getattr(player, 'name', 'Jugador')}: stat_modifier={getattr(player, 'stat_modifier', 1.0)}")
    # PvP weapon theft logic
    def can_steal_weapon(self, target_player):
        """Determina si se puede robar un arma al jugador objetivo según reglas de protección."""
        # Regla: No se puede robar si el jugador objetivo está protegido
        protection = getattr(target_player, 'weapon_protection_until', None)
        from datetime import datetime
        if protection and datetime.now() < protection:
            print("El jugador está protegido. No puedes robarle el arma.")
            return False
        # Regla: No se puede robar si el jugador no tiene arma
        owned_weapons = getattr(target_player, 'owned_weapons', [])
        if not owned_weapons:
            print("El jugador no tiene armas para robar.")
            return False
        return True

    def steal_weapon(self, target_player):
        """Roba un arma al jugador objetivo si las reglas lo permiten."""
        if not self.can_steal_weapon(target_player):
            return False
        # Solo puede robar una arma
        stolen_weapon = target_player.owned_weapons.pop(0)
        if not hasattr(self.player, 'owned_weapons'):
            self.player.owned_weapons = []
        self.player.owned_weapons.append(stolen_weapon)
        # Protege al jugador objetivo por 24h
        from datetime import datetime, timedelta
        target_player.weapon_protection_until = datetime.now() + timedelta(hours=24)
        print(f"Has robado el arma '{stolen_weapon}' a {getattr(target_player, 'name', 'otro jugador')}. Protegido por 24h.")
        return True
    # Fragment shop logic
    def get_fragment_price(self, item_name):
        """Devuelve el precio en fragmentos según si el ítem/arma es de la facción del jugador o de otra."""
        faction_items = [
            'Cáliz de la Salvación Eterna',
            'Espada del Juicio Final',
            'Escudo de la Fe',
            'Armadura de la Cruz',
            'Lanza de la Redención',
            'Corona de la Gloria'
        ]
        if item_name in faction_items and self.faction == 'cruzado':
            return 50
        elif item_name in faction_items and self.faction != 'cruzado':
            return 100
        # Puedes expandir para otras facciones
        return 100

    def can_buy_item(self, item_type):
        """Solo puede tener 1 item y 1 arma."""
        owned_items = getattr(self.player, 'owned_items', [])
        owned_weapons = getattr(self.player, 'owned_weapons', [])
        if item_type == 'item' and len(owned_items) >= 1:
            return False
        if item_type == 'weapon' and len(owned_weapons) >= 1:
            return False
        return True

    def buy_fragment_shop_item(self, item_name, item_type):
        """Compra un ítem/arma si cumple las reglas de fragmentos y propiedad."""
        price = self.get_fragment_price(item_name)
        fragments = getattr(self.player, 'fragments', {})
        fragment_type = f"Fragmento de {item_name.split(' ')[-1]}"
        if fragments.get(fragment_type, 0) < price:
            print(f"No tienes suficientes fragmentos para comprar {item_name}.")
            return False
        if not self.can_buy_item(item_type):
            print(f"Ya tienes un {item_type}. Solo puedes tener uno.")
            return False
        fragments[fragment_type] -= price
        if item_type == 'item':
            if not hasattr(self.player, 'owned_items'):
                self.player.owned_items = []
            self.player.owned_items.append(item_name)
        elif item_type == 'weapon':
            if not hasattr(self.player, 'owned_weapons'):
                self.player.owned_weapons = []
            self.player.owned_weapons.append(item_name)
        print(f"Has comprado {item_name} por {price} fragmentos.")
        return True

    def fragment_shop_disappear(self):
        """La tienda desaparece si se compran los 6 artículos."""
        owned_items = getattr(self.player, 'owned_items', [])
        owned_weapons = getattr(self.player, 'owned_weapons', [])
        total_owned = len(owned_items) + len(owned_weapons)
        if total_owned >= 6:
            print("La tienda de fragmentos ha desaparecido. Ahora solo puedes robar artículos en eventos especiales.")
            return True
        return False

    # War registration logic
    def register_for_war(self, side):
        """Registra al jugador en un bando para la guerra santa."""
        self.player.war_side = side
        print(f"Jugador registrado en el bando: {side}")

    def get_max_distribution(self):
        """Devuelve la máxima distribución posible en guerras: 4 de un bando y 2 del otro."""
        return {'max_per_side': 4, 'min_per_side': 2}
    def __init__(self, faction_name, player):
        self.faction = faction_name
        self.current_mission = 1
        self.previous_builds = []
        self.player = player
        self.ad_manager = AdManager()
        self.faith_pass = FaithPass(player)
        self.progression_limits = ProgressionLimits(player, self.faith_pass)
        self.deity_selected = False

    def start_next_mission(self):
        if not self.progression_limits.can_start_mission():
            print('Has alcanzado el límite diario de misiones.')
            return
        if self.current_mission <= 3:
            build = PRESET_BUILDS[self.faction][self.current_mission]
            self._launch_mission(build)
        elif not self.deity_selected:
            # Selección de ultimate/deidad tras tutorial
            DeitySelectionUI(self.faction, on_select=self._select_deity)
        else:
            BuildSelection(
                faction_name=self.faction,
                on_confirm=self._launch_mission
            )

    def _select_deity(self, deity):
        self.player.deity = deity
        self.player.passive = deity['passive']
        self.player.ultimate = deity['ultimate']
        self.player.ultimate_desc = deity['ultimate_desc']
        self.player.moral = 0
        self.deity_selected = True
        print(f"Deidad/Ultimate seleccionada: {deity['name']}")
        self.start_next_mission()

    def _launch_mission(self, build):
        self.previous_builds.append(build.copy())
        self.player = Player(self.faction, build, position=(0,0,0))
        print(f'Iniciando misión {self.current_mission} con build:', build)
        self.ad_manager.show_banner()
        if self.ad_manager.should_show_popup():
            self.ad_manager.show_popup()
        # Aquí cargas cámara, enemigos, UI, etc.

    def complete_mission(self):
        self.current_mission += 1
        self.progression_limits.complete_mission()
        self.start_next_mission()
