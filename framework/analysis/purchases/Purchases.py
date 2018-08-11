from datetime import datetime
import json
from framework.analysis.Result import Result


class Purchases(Result):

    def __init__(self, title):
        self.title = title
        self.created_at = datetime.now()
        self.shopping_cards = []

    def add(self, shopping_card):
        self.shopping_cards.append(shopping_card)

    def to_json(self):
        result = {
            "type": "purchases",
            "title": self.title,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "shopping_cards": []
        }

        shopping_card_list = []
        for shopping_card in self.shopping_cards:
            shopping_card_dict = {
                "id": shopping_card.id,
                "invoice_address": shopping_card.invoice_address,
                "shipping_address": shopping_card.shipping_address,
                "shipping": shopping_card.shipping,
                "articles": []
            }
            for article in shopping_card.articles:
                shopping_card_dict['articles'].append({
                    "name": article.name,
                    "description": article.description,
                    "amount": article.amount,
                    "total": article.total,

                })
            shopping_card_list.append(shopping_card_dict)

        result['shopping_cards'] = shopping_card_list

        return json.dumps(result)

