#!/usr/bin/env python3
"""
USSD Language Selector for Imperial Network
"""
import sys
from pathlib import Path

# Add the parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lang.language_config import lang

class USSDLanguageHandler:
    def __init__(self, session_id, phone_number):
        self.session_id = session_id
        self.phone_number = phone_number
        self.current_lang = self.get_user_language()
    
    def get_user_language(self):
        """Get user's preferred language (would query DB in production)"""
        # For demo, infer from village or phone prefix
        if self.phone_number.startswith('079'):
            return 've'  # Thohoyandou area (Tshivenda)
        elif self.phone_number.startswith('082'):
            return 'ts'  # Malamulele area (Xitsonga)
        elif self.phone_number.startswith('083'):
            return 'en'  # Default English
        else:
            return 'en'   # Default
    
    def get_welcome(self):
        """Get welcome message in user's language"""
        return lang.get_text('ussd_menu_welcome', self.current_lang)
    
    def get_main_menu(self):
        """Get main menu in user's language"""
        return lang.get_text('ussd_menu_main', self.current_lang)
    
    def get_language_menu(self):
        """Get language selection menu"""
        menu = lang.get_text('menu_language', self.current_lang) + "\n"
        for l in lang.list_available_languages():
            menu += f"{l['code']}. {l['flag']} {l['name']}\n"
        return menu
    
    def process_input(self, user_input):
        """Process USSD input with language awareness"""
        if user_input == '5':  # Language option
            return self.get_language_menu()
        elif user_input in ['1', '2', '3']:  # Language selection
            lang_map = {'1': 'en', '2': 've', '3': 'ts'}
            if user_input in lang_map:
                self.current_lang = lang_map[user_input]
                return f"Language set to {lang.languages[self.current_lang]['name']}\n" + self.get_main_menu()
        return None

# Test the language system
if __name__ == "__main__":
    print("🏛️ TESTING MULTI-LANGUAGE SUPPORT")
    print("=" * 50)

    # Test different phones
    test_phones = ['0791234567', '0821234567', '0831234567']

    for phone in test_phones:
        handler = USSDLanguageHandler('test', phone)
        print(f"\n📱 Phone: {phone}")
        print(f"   Language: {handler.current_lang}")
        print(f"   Welcome: {handler.get_welcome()}")
        print(f"   Main Menu:\n{handler.get_main_menu()}")

    # Test language switching
    print("\n🔄 Testing language switch:")
    handler = USSDLanguageHandler('test', '0791234567')
    print(f"Initial: {handler.get_main_menu()}")
    print("\nAfter selecting Tshivenda:")
    result = handler.process_input('2')
    print(result)
