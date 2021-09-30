#coding:utf-8
#!/usr/bin/python3.8.10
#filename : memoryManager.py

"""
ce fichier contiendra toutes les méthodes pour faire l'interface entre l'interface graphique et la mémoire
structure standard de la mémoire :(fichier json)
{
    "<numéro de semaine>":{
        "lundi": {
                "<event name>": {
                    "name":"",
                    "begin":"",
                    "end":"",
                    "location":"",
                    "notes":"",
                    "coordinates":(0, 0, 0, 0),
                    "color":""
            },
            ...
        },
        "mardi": <voir lundi>,
        "mercredi": <voir lundi>,
        "jeudi": <voir lundi>;
        "vendredi": <voir lundi>,
        "samedi": <voir lundi>,
        "dimanche": <voir lundi>
    },
    ...
}
"""

import json
from datetime import datetime
DAYST = ("lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche")

def init_week(file: dict):
    date = datetime.now()
    week_id = datetime.date(date[0], date[1], date[2]).isocalendar()
    file = {
        week_id:{
            "lundi": None,
            "mardi": None,
            "mercredi": None,
            "jeudi": None,
            "vendredi": None,
            "samedi": None,
            "dimanche": None
        }
    }
    return file

def getMemory(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)

def writeMemory(file: dict, content: dict, path: str):
    new_content = {
        "name":content["name"].replace("\n", "") if content["name"]!=None else None,
        "begin":content["begin"].replace("\n", "") if content["begin"]!=None else None,
        "end":content["end"].replace("\n", "") if content["end"]!=None else None,
        "location":content["location"].replace("\n", "") if content["location"]!=None else None,
        "notes":content["notes"].replace("\n", "") if content["notes"]!=None else None,
        "coordinates":content["coordinates"],
        "color": content["color"].replace("\n", "") if content["color"]!=None else None
    }
    file["week"][content["day"].replace("\n", "")][content["name"].replace("\n", "")] = content

    with open(path, 'w', encoding='utf-8') as json_file:
        json.dump(file, json_file, indent=3)

def getEventListOfTheDay(file: dict, day: str) -> dict:
    event_list = []
    day_events = file["week"][day]
    for event in day_events:
        event_list.append(day_events[event])
    
    return event_list

def getCoordinatesDict(file: dict) -> dict:
    coordinates_dict = {
            "lundi": {},
            "mardi": {},
            "mercredi": {},
            "jeudi": {},
            "vendredi": {},
            "samedi": {},
            "dimanche": {}
        }
    file = file["week"]
    for day in DAYST:
        for event in file[day]:
            coordinates_dict[day][file[day][event]["name"]] = file[day][event]["coordinates"]
    
    return coordinates_dict

def delete(file, event, day, path):
    file["week"][day].pop(event, None)
    with open(path, 'w', encoding='utf-8') as json_file:
        json.dump(file, json_file, indent=3)

if __name__ == "__main__":
    print(getCoordinatesDict(getMemory("memory/currentEdt.json")))