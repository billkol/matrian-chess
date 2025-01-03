class Rooms:
    def __init__(self):
        self.rooms = {
            'Data': [1, 11102]
        }

    def new_user(self):
        return [i for i in self.rooms if self.rooms[i][0] == 1]

    def the_open_room(self, name_room):
        if name_room in self.rooms:
            return self.rooms[name_room]

    def open_game_in_the_room(self, name_room, chat_id):
        if name_room not in self.rooms:
            self.rooms[name_room] = [1, chat_id]
