import json
from framework.analysis.Result import Result


class Timeline(Result):

    def __init__(self, title):
        self.title = title
        self.elements = []

    def add(self, element):
        self.elements.append(element)

    def to_json(self):
        result = {
            "type": "timeline",
            "title": self.title,
            "elements": []
        }
        for element in self.elements:
            result['elements'].append({
                "datetime": element.datetime.strftime("%Y-%m-%d %H:%M:%S"),
                "title": element.title,
                "content": element.content,
            })

        return json.dumps(result)

