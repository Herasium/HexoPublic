from __main__ import hexo  
import firebase_admin
from firebase_admin import credentials, db
import json

functions = {}

cred = credentials.Certificate(hexo.secrets["key"])
default_app = firebase_admin.initialize_app(cred, {
	'databaseURL':hexo.secrets["url"]
})

hexo.db = db