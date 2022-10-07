class Item:
    def __init__(self, id, title, status, created):
        self.title = title
        self.status = status
        self.created = created
        self.id = id

    @classmethod
    def from_mongo_item(cls, item):
        return cls(item['_id'], item['title'], item['status'], item['created'])