import os
import json

LOCALES = {}

def load_locales():
    global LOCALES
    for file in os.listdir("locales"):
        if file.endswith(".json"):
            lang_code = file.split(".")[0]
            with open(os.path.join("locales", file), "r", encoding="utf-8") as f:
                LOCALES[lang_code] = json.load(f)

load_locales()
