#!/usr/bin/env python3
"""
🏛️ IMPERIAL MULTI-LANGUAGE SUPPORT SYSTEM
Languages: English, Tshivenda, Xitsonga
"""
import json
from pathlib import Path

class ImperialLanguages:
    def __init__(self):
        self.languages = {
            'en': {
                'name': 'English',
                'code': 'en',
                'flag': '🇬🇧',
                'active': True
            },
            've': {
                'name': 'Tshivenda',
                'code': 've',
                'flag': '🏔️',
                'active': True
            },
            'ts': {
                'name': 'Xitsonga',
                'code': 'ts',
                'flag': '🌊',
                'active': True
            }
        }
        self.default_lang = 'en'
        self.translations = self.load_translations()
    
    def load_translations(self):
        """Load all translation files"""
        trans_dir = Path(__file__).parent / 'translations'
        translations = {}
        
        for lang_code in self.languages.keys():
            lang_file = trans_dir / f'{lang_code}.json'
            if lang_file.exists():
                with open(lang_file, 'r') as f:
                    translations[lang_code] = json.load(f)
            else:
                translations[lang_code] = {}
        
        return translations
    
    def get_text(self, key, lang=None):
        """Get translated text for key in specified language"""
        if not lang or lang not in self.languages:
            lang = self.default_lang
        
        # Try requested language
        if lang in self.translations and key in self.translations[lang]:
            return self.translations[lang][key]
        
        # Fallback to English
        if 'en' in self.translations and key in self.translations['en']:
            return self.translations['en'][key]
        
        # Ultimate fallback
        return key
    
    def get_ussd_menu(self, menu_name, lang=None):
        """Get USSD menu in specified language"""
        return self.get_text(f'ussd_menu_{menu_name}', lang)
    
    def get_notification(self, notif_type, lang=None):
        """Get notification template in specified language"""
        return self.get_text(f'notif_{notif_type}', lang)
    
    def get_village_greeting(self, village, lang=None):
        """Get village-specific greeting"""
        return self.get_text(f'greeting_{village}', lang)
    
    def list_available_languages(self):
        """Return list of active languages"""
        return [{'code': k, 'name': v['name'], 'flag': v['flag']} 
                for k, v in self.languages.items() if v['active']]

# Global instance
lang = ImperialLanguages()
