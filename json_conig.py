
import json

settings_json = json.dumps([{'type': 'bool', 'title': 'Hint on/off', 'desc': 'Display hints to help you play the game', 'section': 'settings', 'key': 'hint'},
	{'type': 'bool', 'title': 'Sound on/off', 'desc': 'Have some good music to play along', 'section': 'settings', 'key': 'music'},
	{'type': 'bool', 'title': 'AI on/off', 'desc': 'Compete against an AI', 'section': 'settings', 'key': 'ai'}])