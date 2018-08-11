class Conversation:

    last_id = 0

    def __init__(self):
        Conversation.last_id += 1
        self.id = Conversation.last_id
        self.messages = []

    def add(self, message):
        self.messages.append(message)
