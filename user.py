#coding:utf-8
#!/usr/bin/python3.8.10
#filename : user.py

#génération du self.profil utilisateur
import json

class User:
    def __init__(self):
        with open("memory/DefaultValues.json", "r", encoding="utf-8") as def_val:
            default_values = json.load(def_val)
        self.THEME = default_values["THEME"]
        self.username = default_values["PROFIL"]["NAME"]