import os
import json

CURR_LANG = 'en_us'
base_dir = os.path.dirname(os.path.abspath(__file__))  # Absolute path to the current script's directory
lang_path = os.path.join(base_dir, '..', 'resources', 'Langs', f'{CURR_LANG}.json')

with open(lang_path, 'r') as file:
    translation = json.load(file)

ROOT_TITLE = translation['root']['title']
