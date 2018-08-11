class Participant:

    last_id = 0

    def __init__(self, name):
        Participant.last_id += 1
        self.id = Participant.last_id
        self.name = name
