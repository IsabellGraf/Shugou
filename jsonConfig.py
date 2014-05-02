
import json

settingsjson = json.dumps([{'type': 'bool', 'title': 'Hint on/off', 'desc': 'Display hints to help you play the game', 'section': 'settings', 'key': 'hint'},
	{'type': 'bool', 'title': 'Sound on/off', 'desc': 'Have some good music to play along', 'section': 'settings', 'key': 'sound'},
	{'type': 'bool', 'title': 'AI on/off', 'desc': 'Compete against an AI', 'section': 'settings', 'key': 'ai'},
	{'type': 'options', 'title': 'Hint speed', 'desc': 'Speed of the hint', 'options':['slow','normal','fast'], 'section': 'settings', 'key': 'hintspeed'}])