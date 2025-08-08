import json
import os

class DataManager:
    def __init__(self):
        self.missions = {}
        self.items = {}
        # ... otros tipos de datos que quieras cargar

    def load_all_data(self):
        print("Cargando todos los datos del juego...")
        self._load_folder_data('data/missions', self.missions)
        self._load_folder_data('data/items', self.items)
        print("Datos cargados exitosamente.")

    def _load_folder_data(self, folder_path, data_dictionary):
        """Función genérica para cargar todos los JSON de una carpeta."""
        for filename in os.listdir(folder_path):
            if filename.endswith('.json'):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    try:
                        data = json.load(f)
                        # Usamos el 'id' dentro del JSON como clave del diccionario
                        if 'id' in data:
                            data_dictionary[data['id']] = data
                        else:
                            print(f"Advertencia: El archivo {filename} no tiene un 'id'.")
                    except json.JSONDecodeError:
                        print(f"Error: El archivo {filename} no es un JSON válido.")

    def get_mission(self, mission_id):
        return self.missions.get(mission_id)

    def get_item(self, item_id):
        return self.items.get(item_id)
