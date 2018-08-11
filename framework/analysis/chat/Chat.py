from datetime import datetime
import json
from framework.analysis.Result import Result


class Chat(Result):

    def __init__(self, title):
        self.title = title
        self.created_at = datetime.now()
        self.conversations = []

    def add(self, conversation):
        self.conversations.append(conversation)

    def to_json(self):
        result = {
            "type": "chat",
            "title": self.title,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "conversations": []
        }

        conversation_list = []
        for conversation in self.conversations:
            conversation_dict = {
                "id": conversation.id,
                "messages": []
            }
            for message in conversation.messages:
                conversation_dict['messages'].append({
                    "participant": {
                        "id": message.participant.id,
                        "name": message.participant.name
                    },
                    "datetime": message.datetime.strftime("%Y-%m-%d %H:%M:%S"),
                    "content": message.content
                })
            conversation_list.append(conversation_dict)

        result['conversations'] = conversation_list

        return json.dumps(result)

