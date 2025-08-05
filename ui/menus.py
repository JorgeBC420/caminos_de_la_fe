from systems.lang_manager import _
from ursina import Button, color

def create_main_menu():
    Button(text=_("play_button"), color=color.azure)
    Button(text=_("options_button"), color=color.orange)
    Button(text=_("exit_button"), color=color.red)
