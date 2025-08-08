from data.missions import load_mission_json
from ursina import *

class MissionManager:
    def __init__(self, player_faction):
        self.player_faction = player_faction
        self.current_mission_id = None
        self.completed_missions = set()
        self.available_side_quests = []
        self.active_mission_data = None


    def load_mission(self, mission_id):
        """
        Carga una misión individual desde data/missions/{mission_id}.json
        """
        return load_mission_json(mission_id)

    def get_side_quests(self):
        return self.available_side_quests

    def start_mission(self, mission_id):
        missions = self.get_main_missions()
        mission = next((m for m in missions if m['id'] == mission_id), None)
        if mission:
            self.current_mission_id = mission_id
            self.active_mission_data = mission
            return mission
        return None

    def complete_mission(self, player):
        if self.active_mission_data:
            self.completed_missions.add(self.current_mission_id)
            rewards = self.active_mission_data.get('rewards', {})
            player.add_experience(rewards.get('xp', 0))
            player.add_gold(rewards.get('gold', 0))
            for item in rewards.get('items', []):
                player.add_item(item)
            self.active_mission_data = None
            self.current_mission_id = None

    def save_state(self):
        return {
            'current_mission_id': self.current_mission_id,
            'completed_missions': list(self.completed_missions),
            'available_side_quests': self.available_side_quests
        }

    def load_state(self, state):
        self.current_mission_id = state.get('current_mission_id')
        self.completed_missions = set(state.get('completed_missions', []))
        self.available_side_quests = state.get('available_side_quests', [])
