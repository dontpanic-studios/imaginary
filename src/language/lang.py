from enum import Enum, auto
from dotenv import load_dotenv
import json, os

class LanguageList(Enum): # oh no
    NO_DESCRIPTION_FOUND = auto()
    NO_ARGUMENTS_FOUND = auto()
    NO_METADATA_FOUND = auto()
    NO_VM_AVALIABLE = auto()
    NO_VM_AVALIABLE_DESC = auto()
    MAIN_STATUS_NULL = auto()
    SELECT_VM = auto()
    MAIN_STATUS_RUNNING = auto()
    DUMMY = auto()
    MAIN_VMSTART = auto()
    MAIN_VMEDIT = auto()
    CREATEVM_3_TITLE = auto()
    CREATEVM_2_TITLE = auto()
    CREATEVM_1_TITLE = auto()
    CREATE_VM = auto()
    IMAGINARY_INFO = auto()
    DISK_TOOL = auto()
    FORCE_RELOAD_LIST = auto()


class Language():
    def __init__():
        pass

    def getLanguageByEnum(lang: LanguageList):
        load_dotenv('./data/setting.env')
        curLang = os.environ.get('Language')
        lang_file = open(f'data/language/{curLang}.json', "r+", encoding="utf-8")
        data = json.load(lang_file)

        return data[lang.name]