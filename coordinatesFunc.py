#coding:utf-8
#!/usr/bin/python3.8.10
#filename : coordinatesFunc.py

def isInRectangle(x: int, y: int, rectangle_coordinates: tuple) -> bool:
    if (x >= rectangle_coordinates[0] and 
        x <= rectangle_coordinates[2] and 
        y >= rectangle_coordinates[1] and 
        y <= rectangle_coordinates[3]):

        return True
    else:
        return False

def verifyMousePosition(event, edt_file, DAYST):
    x, y = event.x, event.y
    for day in DAYST:
        for event in edt_file[day]:
            if isInRectangle(x, y, edt_file[day][event]):
                return (day, event)
    
    return False

def format_time(time: str) -> float:
    try:
        hour = time[:2]
        mins = time[3:]

        #format mins to coordinates
        if mins[0] == "0":
            mins = int(mins)
            mins = int(round((mins*100)/60))
            mins = "0" + str(mins)
        else:
            mins = int(mins)
            mins = int(round((mins*100)/60))

        final_y = float(hour + "." + str(mins))

        return final_y
    except:
        print("ERREUR DE SAISIE")

if __name__ == "__main__":
    test_rectangle = (480,
                    340.0,
                    640,
                    400.0)

    print(isInRectangle(0, 0, test_rectangle))