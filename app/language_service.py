import json
from pathlib import Path

LANGUAGE_DIR = Path(__file__).parent / "languages"
SUPPORTED_LANGUAGES = {
    "1": "en", "2": "zu", "3": "xh", "4": "st", "5": "af", "6": "sw"
}
LANGUAGE_LABELS = {
    "en": "English", "zu": "isiZulu", "xh": "isiXhosa",
    "st": "Sesotho", "af": "Afrikaans", "sw": "Kiswahili"
}

def load_language(code: str) -> dict:
    path = LANGUAGE_DIR / f"{code}.json"
    if not path.exists():
        path = LANGUAGE_DIR / "en.json"
    return json.loads(path.read_text(encoding="utf-8"))

def translate(language: str, key: str, **kwargs) -> str:
    data = load_language(language)
    template = data.get(key) or load_language("en").get(key, key)
    return template.format(**kwargs)
