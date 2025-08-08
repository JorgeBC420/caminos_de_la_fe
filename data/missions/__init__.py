import json
import os

def load_mission_json(mission_id):
    """
    Carga un archivo de misión individual por ID desde data/missions/.
    """
    path = os.path.join(os.path.dirname(__file__), 'missions', f'{mission_id}.json')
    if not os.path.exists(path):
        raise FileNotFoundError(f"No se encontró la misión: {path}")
    with open(path, encoding='utf-8') as f:
        return json.load(f)
