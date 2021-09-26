#coding:utf-8


def isInRectangle(x: int, y: int, rectangle_coordinates: tuple) -> bool:
    if (x >= rectangle_coordinates[0] and 
        x <= rectangle_coordinates[2] and 
        y >= rectangle_coordinates[1] and 
        y <= rectangle_coordinates[3]):

        return True
    else:
        return False

if __name__ == "__main__":
    test_rectangle = (480,
                    340.0,
                    640,
                    400.0)

    print(isInRectangle(0, 0, test_rectangle))