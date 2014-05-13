
import json

settingsjson = json.dumps([
	{'type': 'bool', 'title': 'Sound on/off', 'desc': 'Have some good music to play along', 'section': 'settings', 'key': 'sound'},
	{'type': 'bool', 'title': 'AI on/off', 'desc': 'Compete against an AI', 'section': 'settings', 'key': 'ai'},
	{'type': 'options', 'title': 'Hint', 'desc': 'Control frequency of hint', 'options':['off', 'slow','normal','fast'], 'section': 'settings', 'key': 'hint'},
	{'type': 'title', 'title': 'Email bugs and ideas for improvement: \n shugou.app@gmail.com'}])
