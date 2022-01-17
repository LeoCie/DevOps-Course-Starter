class Item:
    def __init__(self, id, title, status):
        self.title = title
        self.status = status
        self.id = id

    @classmethod
    def from_trello_card(cls, card, status):
        return cls(card['id'], card['name'], status)