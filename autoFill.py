#coding:utf-8
#!/usr/bin/python3.8.10
#filename : autoFill.py
"""
fonctions pour améliorer l'expérience utilisateur en autoremplissant certains champs en fonction de l'endroit cliqué

"""
import coordinatesFunc as coo
from math import floor

DAYSCOO = {"lundi": (0, 0, 160, 602),
        "mardi": (160, 0, 160*2, 602), 
        "mercredi": (160*2, 0, 160*3, 602), 
        "jeudi": (160*3, 0, 160*4, 602), 
        "vendredi": (160*4, 0, 160*5, 602), 
        "samedi": (160*5, 0, 160*6, 602), 
        "dimanche": (160*6, 0, 160*7, 602)}

#fonction pour trouver si le clic est effectué sur un jour précis
def findDay(x: int, y: int) -> str:
    global DAYSCOO

    for key, value in DAYSCOO.items():
        if coo.isInRectangle(x, y, value):
            return key
    return None

def findHour(y:int) -> tuple:

    hour = floor((y-40)/40 + 6)
    return str(hour)+"h00", str(hour + 1)+"h00"

if __name__ == "__main__":
    print(findHour(400))