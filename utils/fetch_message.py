
from utils.load_locales import LOCALES

USER_LANG = {}

def get_message(key, user_id):
    """
    Fetch a message by key and language.
    
    Args:
        key (str): The message key (e.g., 'cancel', 'usage_instructions')
        lang (str): Language code ('en', 'ar', etc.)
    
    Returns:
        str: The translated message, or key if not found.
    """
    def get_user_lang(user_id):
        return USER_LANG.get(user_id, "en")

    return LOCALES.get(get_user_lang(user_id), {}).get(key, LOCALES["en"].get(key, key))
