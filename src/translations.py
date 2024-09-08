import json
import os

CURR_LANG = 'en_us'

with open(os.path.join('resources', 'langs', f'{CURR_LANG}.json'), 'r') as file:
    translation = json.load(file)

ROOT_TITLE = translation['root']['title']