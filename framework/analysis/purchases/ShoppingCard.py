class ShoppingCard:

    last_id = 0

    def __init__(self, invoice_address, shipping_address, shipping):
        ShoppingCard.last_id += 1
        self.id = ShoppingCard.last_id
        self.invoice_address = invoice_address
        self.shipping_address = shipping_address
        self.shipping = shipping
        self.articles = []

    def add(self, article):
        self.articles.append(article)
