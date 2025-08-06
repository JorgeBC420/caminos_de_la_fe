import json
import os
import locale
from ursina import *

class LanguageManager:
    _instance = None
    current_language = {}
    SUPPORTED_LANGUAGES = ['es', 'en', 'de', 'fr', 'it', 'pt', 'ar']
    DEFAULT_LANGUAGE = 'en'

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LanguageManager, cls).__new__(cls)
            cls._instance._init_manager()
        return cls._instance

    def _init_manager(self):
        self.set_language(self._detect_system_language())

    def _detect_system_language(self):
        try:
            sys_lang, _ = locale.getlocale()
            if sys_lang and sys_lang[:2].lower() in self.SUPPORTED_LANGUAGES:
                return sys_lang[:2].lower()
        except Exception as e:
            print(f"Error detecting system language: {e}")
        return self.DEFAULT_LANGUAGE

    def set_language(self, lang_code):
        if lang_code not in self.SUPPORTED_LANGUAGES:
            lang_code = self.DEFAULT_LANGUAGE
        file_path = os.path.join('localization', f'{lang_code}.json')
        if not os.path.exists(file_path):
            print(f"Language file not found: {file_path}")
            return
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.current_language = json.load(f)
            print(f"Language set to: {lang_code}")
        except Exception as e:
            print(f"Error loading language: {e}")
            self.current_language = {}

    def get_text(self, key):
        return self.current_language.get(key, f"[{key}_MISSING]")

# Singleton global
lang_manager = LanguageManager()

def _(key):
    return lang_manager.get_text(key)
