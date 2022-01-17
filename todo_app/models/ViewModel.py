class ViewModel:
    def __init__(self, items):
        self._items = items

    @property
    def items(self):
        return self._items

    @property
    def to_do_items(self):
        return [item for item in self._items if item.status == 'Not Started']

    @property
    def in_progress_items(self):
        return [item for item in self._items if item.status == 'In Progress']

    @property
    def completed_items(self):
        return [item for item in self._items if item.status == 'Done']