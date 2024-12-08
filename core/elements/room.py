import display_config as config

class Room:
    def __init__(self, x, y, number, side="LEFT"):
        self.x = x
        self.y = y
        self.number = number

        if side=="LEFT":
            list_beds = [(x + 1, y + config.ROOM_HEIGHT - 4), (x + config.BED_WIDTH + 3, y + config.ROOM_HEIGHT - 4)]
            list_desks = [(x + 1, y + 1), (x + config.BED_WIDTH + 3, y + 1)]
        else:
            list_beds = [(x + 4, y + config.ROOM_HEIGHT - 4), (x + config.ROOM_WIDTH - config.BED_WIDTH - 1, y + config.ROOM_HEIGHT - 4)]
            list_desks = [(x + 4, y + 1), (x + config.ROOM_WIDTH - config.BED_WIDTH - 1, y + 1)]

        self.beds = list_beds  # Bed positions
        self.desks = list_desks  # Desk positions