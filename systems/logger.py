import logging
import os

LOG_FILE = 'game.log'
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s'
)

def log_debug(msg):
    logging.debug(msg)

def log_error(msg):
    logging.error(msg)

# Ejemplo de uso:
# log_debug('Inventario cargado correctamente')
# log_error('Error al cargar textura')
