#coding:utf-8
#!/usr/bin/python3.8.10
#filename : main.py
"""
auteur : Gerald Pellegrino || ჯExypnoseinT²NaHჯ#2946

ce fichier main est celui qui sert à lancer l'application et contient la class Fenetre qui génère la fenetre
principale, il a besoin des fichiers user.py, memoryManager.py et coordinatesFunc.py pour fonctionner
"""

from tkinter import *
import memoryManager as mm
import coordinatesFunc as coo
from user import User
from autoFill import findDay, findHour

#intialisation des variables d'environnement
DAYST = ("lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche")
color_en = {
            "rouge": "red",
            "jaune": "yellow",
            "vert": "green",
            "bleu": "blue",
            "marron": "brown",
            "rose": "pink",
            "violet": "purple"
        }

class Fenetre:
    def __init__(self, profil):
        self.profil = profil
        self.fenetre = Tk()
        self.fenetre.geometry("2704x1230")
        self.fullScreenState = False
        self.fenetre.bind("<F11>", self.toggleFullScreen)
        self.fenetre.bind("<Escape>", self.quitFullScreen)
        self.fenetre.config(bg=self.profil["BACKGROUND_COLOR"])
        self.fenetre.title("Gestionnaire d'emploi du temps")


        #generation du fond de l'emploi du temps
        self.mainFrame = Frame(self.fenetre, bg=self.profil["ACTIVE_BACKGROUND_COLOR"]).pack()
        self.edtCanv = Canvas(self.mainFrame, 
                                height=602, 
                                width=1130, 
                                bg=self.profil["ACTIVE_BACKGROUND_COLOR"])
        self.edtCanv.bind("<ButtonPress-1>", self.initiateAddOrRemove)

        self.edtCanv.pack(padx=50, pady=50)

        for i in range(1, 7):
            self.edtCanv.create_line(i*160, 0, i*160, 602, fill=self.profil["WIDGET_COLOR"])
        for i in range(1, 15):
            if i != 1:
                self.edtCanv.create_line(0, i*40, 1130, i*40, fill=self.profil["WIDGET_COLOR"], width=1, dash=(3, 1))
            else:
                self.edtCanv.create_line(0, i*40, 1130, i*40, fill=self.profil["WIDGET_COLOR"], width=1)
        for i in range(len(DAYST)):
            self.edtCanv.create_text(i*160+80, 0, anchor='n', fill=self.profil["TEXT_COLOR"], font=("helvetica", 20), text=DAYST[i])
        
        self.getMemoryEdt()

        self.fenetre.mainloop()
    
    def toggleFullScreen(self, event):
        self.fullScreenState = not self.fullScreenState
        self.fenetre.attributes("-fullscreen", self.fullScreenState)
    
    def quitFullScreen(self, event):
        self.fullScreenState = False
        self.fenetre.attributes("-fullscreen", self.fullScreenState)
    
    def verifyMousePosition(self, event, edt_file) -> bool:
        return coo.verifyMousePosition(event, edt_file, DAYST)
    
    def initiateAddOrRemove(self, event):
        result = self.verifyMousePosition(event, mm.getCoordinatesDict(mm.getMemory("memory/currentEdt.json")))
        if not result:
            self.addEvent(event)
        else:
            self.modifyRemoveEvent(result[0], result[1])

    def modifyRemoveEvent(self, day, _event):

        def preview_event(element, previewCanvas):
            previewCanvas.create_rectangle(0, 0, 160, 80, fill=color_en[element["color"]])

            eventName = Text(previewCanvas, bg=color_en[element["color"]], relief="flat")
            eventName.config(width=len(element["name"]), height=1)
            eventName.insert(INSERT, element["name"])
            eventName.place(x=80, y=20, anchor="center")

            eventBegin = Text(previewCanvas, bg=color_en[element["color"]], relief="flat")
            eventBegin.config(width=len(element["begin"]), height=1)
            eventBegin.insert(INSERT, element["begin"])
            eventBegin.place(x=40, y=40, anchor="center")

            eventEnd = Text(previewCanvas, bg=color_en[element["color"]], relief="flat")
            eventEnd.config(width=len(element["end"]), height=1)
            eventEnd.insert(INSERT, element["end"])
            eventEnd.place(x=120, y=40, anchor="center")

            eventLocation = Text(previewCanvas, bg=color_en[element["color"]], relief="flat")
            eventLocation.config(width=len(element["location"]), height=1)
            eventLocation.insert(INSERT, element["location"])
            eventLocation.place(x=80, y=60, anchor="center")
            
            return eventName, eventBegin, eventEnd, eventLocation

        element = mm.getMemory("memory/currentEdt.json")["week"][day][_event]

        self.eventModif = Toplevel(self.fenetre)
        self.eventModif.title("ajouter un évènement")    
        self.eventModif.geometry("400x500")
        self.eventModif.config(bg=self.profil["ACTIVE_BACKGROUND_COLOR"])

        title = Label(self.eventModif, text="modifier l'élément {}".format(element["name"]),
                        font=("helvetica", 14),
                        fg=self.profil["TEXT_COLOR"],
                        bg=self.profil["ACTIVE_BACKGROUND_COLOR"]).pack()
        
        previewCanvas = Canvas(self.eventModif, bg=self.profil["ACTIVE_BACKGROUND_COLOR"], height=80, width=160)
        previewCanvas.pack(pady=30, padx=50)

        eventName, eventBegin, eventEnd, eventLocation = preview_event(element, previewCanvas)

        eventNotesLabel = Label(self.eventModif, text="notes",
                                font=("helvetica", 12),
                                fg=self.profil["TEXT_COLOR"],
                                bg=self.profil["ACTIVE_BACKGROUND_COLOR"]).pack(padx=5, pady=5, side='top')
        NotesEntry = Text(self.eventModif)
        NotesEntry.config(width=30, height=5)
        NotesEntry.insert(INSERT, (element["notes"] if element["notes"] != None else "ajouter des informations supplémentaires"))
        NotesEntry.pack(padx=5, side='top')

        buttonFrame = Frame(self.eventModif, bg=self.profil["ACTIVE_BACKGROUND_COLOR"])
        cancelButton = Button(buttonFrame, text="annuler", command=self.eventModif.destroy).pack(side='left')
        deleteButton = Button(buttonFrame, text="supprimer l'evenement", command= lambda: self.deleteEvent(event=element["name"],
                                                                                                            day=day
        )).pack(side='left', padx=10)
        okButton = Button(buttonFrame, text="valider", command= lambda: self.updateEvent(name = eventName.get("1.0", END),
                                                                                        begin = eventBegin.get("1.0", END),
                                                                                        end = eventEnd.get("1.0", END),
                                                                                        location = eventLocation.get("1.0", END),
                                                                                        notes = NotesEntry.get("1.0", END) if NotesEntry.get("1.0", END) != "ajouter des informations supplémentaires" else None,
                                                                                        day = day,
                                                                                        event = element,
                                                                                        coordinates = element["coordinates"],
                                                                                        color = element["color"]))
        okButton.pack(side='left')
        buttonFrame.pack(side="bottom", pady=10)

    def deleteEvent(self, event, day):
        mm.delete(mm.getMemory("memory/currentEdt.json"), event, day, "memory/currentEdt.json")
        self.clearEdt()
        self.getMemoryEdt()

        self.eventModif.destroy()

    def updateEvent(self, **kwargs):
        changes = False
        update_dict = {}
        for key in kwargs:
            if (key != "coordinates" and key != "event"):
                update_dict[key] = kwargs[key].replace("\n", "")
            else:
                update_dict[key] = kwargs[key]
        update_dict["day"] = kwargs["day"]
        event_ = kwargs["event"]
        for key in event_:
            key.replace("\n", "")

        for key in update_dict:
            if event_.get(key):
                changes = (not event_[key] == update_dict[key])
                if changes:
                    break
        
        if not changes:
            self.eventModif.destroy()
            return
        path = "memory/currentEdt.json"
        mm.writeMemory(mm.getMemory(path), update_dict, path)
        self.clearEdt()
        self.getMemoryEdt()


        self.eventModif.destroy()

    def clearEdt(self):
        self.edtCanv.delete("cible")

    def addEvent(self, event):
        eventAdder = Toplevel(self.fenetre)
        eventAdder.title("ajouter un évènement")    
        eventAdder.geometry("400x300")
        eventAdder.config(bg=self.profil["ACTIVE_BACKGROUND_COLOR"])

        title = Label(eventAdder, text="Ajouter un évènement",
                        font=("helvetica", 14),
                        fg=self.profil["TEXT_COLOR"],
                        bg=self.profil["ACTIVE_BACKGROUND_COLOR"]).pack()

        bigFrame = Frame(eventAdder, bg=self.profil["ACTIVE_BACKGROUND_COLOR"])

        leftFrame = Frame(bigFrame, bg=self.profil["ACTIVE_BACKGROUND_COLOR"])

        eventNameLabel = Label(leftFrame, text="nom de l'évènement",
                                font=("helvetica", 12),
                                fg=self.profil["TEXT_COLOR"],
                                bg=self.profil["ACTIVE_BACKGROUND_COLOR"]).pack(padx=5, pady=5, side='top')
        eventNameEntry = Entry(leftFrame)
        eventNameEntry.pack(padx=5, side='top')

        eventLocationLabel = Label(leftFrame, text="lieu de l'évènement",
                                font=("helvetica", 12),
                                fg=self.profil["TEXT_COLOR"],
                                bg=self.profil["ACTIVE_BACKGROUND_COLOR"]).pack(padx=5, pady=5, side='top')
        eventLocationEntry = Entry(leftFrame)
        eventLocationEntry.pack(padx=5, side='top')

        eventDayLabel = Label(leftFrame, text="Jour de l'évènement",
                                font=("helvetica", 12),
                                fg=self.profil["TEXT_COLOR"],
                                bg=self.profil["ACTIVE_BACKGROUND_COLOR"]).pack(padx=5, pady=5, side='top')
        eventDayEntry = Text(leftFrame, width=15, height=1)
        eventDayEntry.insert(INSERT, findDay(event.x, event.y))
        eventDayEntry.pack(padx=5, side='top')

        leftFrame.pack(side="left", fill=Y)

        """
        BEGINNING OF THE RIGHT FRAME
        """

        rightFrame = Frame(bigFrame, bg=self.profil["ACTIVE_BACKGROUND_COLOR"])

        autoHour = findHour(event.y)
        
        eventBeginLabel = Label(rightFrame, text="heure de début (XXhXX)",
                                font=("helvetica", 12),
                                fg=self.profil["TEXT_COLOR"],
                                bg=self.profil["ACTIVE_BACKGROUND_COLOR"]).pack(padx=5, pady=5, side='top')
        
        entriesBeginFrame = Frame(rightFrame, bg=self.profil["ACTIVE_BACKGROUND_COLOR"])
        hoursbegin = Text(entriesBeginFrame, width=15, height=1)
        hoursbegin.insert(INSERT, autoHour[0])
        hoursbegin.pack(side='left')
        entriesBeginFrame.pack(side="top")

        eventEndLabel = Label(rightFrame, text="heure de fin (XXhXX)",
                                font=("helvetica", 12),
                                fg=self.profil["TEXT_COLOR"],
                                bg=self.profil["ACTIVE_BACKGROUND_COLOR"]).pack(padx=5, pady=5, side='top')

        entriesEndFrame = Frame(rightFrame, bg=self.profil["ACTIVE_BACKGROUND_COLOR"])
        hoursEnd = Text(entriesEndFrame, width=15, height=1)
        hoursEnd.insert(INSERT, autoHour[1])
        hoursEnd.pack(side='left')
        entriesEndFrame.pack(side="top")

        rightFrame.pack(side="right", fill=Y, padx=10)

        bigFrame.pack(side="top")

        colorFrame = Frame(eventAdder, bg=self.profil["ACTIVE_BACKGROUND_COLOR"])

        ColorList = [
            "rouge",
            "jaune",
            "vert",
            "bleu",
            "marron",
            "rose",
            "violet"
        ]

        variable = StringVar(colorFrame)
        variable.set("choisissez la couleur de l'évènement")
        opt = OptionMenu(colorFrame, variable, *ColorList)
        opt.pack(side='top')

        colorFrame.pack(side="top", pady=10)

        buttonFrame = Frame(eventAdder, bg=self.profil["ACTIVE_BACKGROUND_COLOR"])
        cancelButton = Button(buttonFrame, text="annuler", command=eventAdder.destroy).pack(side='left')
        okButton = Button(buttonFrame, text="valider", command=lambda: self.createEvent(eventNameEntry.get(),
                                                                                eventDayEntry.get("1.0", END).replace("\n", ""),
                                                                                variable.get(),
                                                                                hoursbegin.get("1.0", END).replace("\n", ""),
                                                                                hoursEnd.get("1.0", END).replace("\n", ""),
                                                                                eventLocationEntry.get(),
                                                                                eventAdder))
        okButton.pack(side='left', padx=10)
        buttonFrame.pack(side="bottom", pady=10)
    
    def createEvent(self, name: str, day: str, color: str, begin: str, end: str, location: str, eventAdder):
        global DAYST
        global color_en
        DAYST = list(DAYST)

        #format begin
        begin_coordinates = coo.format_time(begin)
        #format end
        end_coordinates = coo.format_time(end)

        #edit event values
        eventValues = {
            "x1": DAYST.index(day if day != "" else 'lundi')*160,
            "y1": ((begin_coordinates) - 6)*40 + 40,
            "x2": DAYST.index(day if day != "" else 'lundi')*160 + 160,
            "y2": ((end_coordinates) - 6)*40 + 40
        }

        #change color to english

        self.edtCanv.create_rectangle(eventValues["x1"],
                                       eventValues["y1"],
                                       eventValues["x2"],
                                       eventValues["y2"], 
                                       fill=color_en[color], tags="cible")
        self.edtCanv.create_text(int(round((eventValues["x1"]+eventValues["x2"])/2)), 
                                    int(round((eventValues["y1"]+eventValues["y2"])/2)),
                                    text="{}\nde {} à {}\nen {}".format(name, begin, end, location),
                                    justify="center", tags="cible")
        
        if eventAdder != "init":
            eventAdder.destroy()

        content_to_memory = {
            "name":name,
            "day":day,
            "begin":begin,
            "end":end,
            "location":location,
            "notes":None,
            "coordinates":[eventValues["x1"], eventValues["y1"], eventValues["x2"], eventValues["y2"]],
            "color": color
        }

        path = "memory/currentEdt.json"
        mm.writeMemory(mm.getMemory(path), content_to_memory, path)

    def getMemoryEdt(self):
        memory = mm.getMemory("memory/currentEdt.json")
        for day in DAYST:
            eventday_list = mm.getEventListOfTheDay(memory, day)
            for event in eventday_list:
                self.createEvent(name=event["name"].replace("\n", ""),
                                    day=day,
                                    color=event["color"].replace("\n", ""),
                                    begin=event["begin"].replace("\n", ""),
                                    end=event["end"].replace("\n", ""),
                                    location=event["location"].replace("\n", ""),
                                    eventAdder="init")


if __name__ == '__main__':
    user = User()
    fenetre = Fenetre(user.THEME)