class MainModel:
    def __init__(self):
        self.data = []

    def add_item(self, item):
        self.data.append(item)

    def remove_item(self, item):
        if item in self.data:
            self.data.remove(item)

    def get_items(self):
        return self.data

    def clear_items(self):
        self.data.clear()