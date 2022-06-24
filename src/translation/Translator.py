from typing import NoReturn
from .de_DE import dictionary as de_DE_dict
from .en_EN import dictionary as en_EN_dict


class Translator:
    def __init__(self):
        self.dictionaries = {}

    def add_dictionary(self, language_code: str, dictionary: dict) -> NoReturn:
        if language_code not in self.dictionaries:
            self.dictionaries[language_code] = dictionary

    def translate(self, language_code: str, key: str) -> str | bool:
        if language_code not in self.dictionaries:
            raise Exception(f"{language_code} not found in dictionary!")

        if key not in self.dictionaries.get(language_code):
            return False

        return self.dictionaries.get(language_code).get(key)

    def get_language_codes(self) -> list[str]:
        return self.dictionaries.keys()

    def get_languages(self) -> list[str]:
        languages = []

        for lang_code, dictionary in self.dictionaries.items():
            languages.append(dictionary.get("self"))

        return languages

    def get_language_by_code(self, language_code: int) -> str | None:
        if language_code not in self.dictionaries:
            return None

        return self.dictionaries.get(language_code).get("self")


# the current language code
language = ""


def set_current_language_code(language_code: str) -> NoReturn:
    global language
    language = language_code


def get_current_language_code() -> str:
    global language
    return language


# the Translator instance singleton
instance = None


def get_instance() -> Translator:
    global instance

    if instance is None:
        instance = Translator()
        instance.add_dictionary("de_DE", de_DE_dict)
        instance.add_dictionary("en_EN", en_EN_dict)
        set_current_language_code("en_EN")

    return instance


# create singleton and translate
def translate(key: str, language_code: str = "", use_fallback: bool = True) -> str | bool:
    translation = get_instance().translate(
        get_current_language_code() if language_code == "" else language_code,
        key
    )

    if translation == False:
        translation = get_instance().translate(
            "en_EN",
            key
        )

    return translation