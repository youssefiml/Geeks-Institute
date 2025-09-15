import math

class Pagination:
    def __init__(self, items = None, page_size = 10):
        if items is None:
            items = []
        self.items = items
        self.page_size = page_size
        self.current_idx = 0
        self.total_pages = math.ceil(len(self.items) / self.page_size)
        
    def get_visible_items(self):
        start_idx = self.current_idx * self.page_size
        end_idx = start_idx + self.page_size
        return self.items[start_idx:end_idx]
    
    def go_to_page(self, page_num):
        page_index = page_num - 1
        if page_index < 0 or page_index >= self.total_pages:
            raise ValueError("Page number out of range")
        self.current_idx = page_index
        
    def first_page(self):
        self.current_idx = 0
        return self
    
    def last_page(self):
        self.current_idx = -1
        return self
    
    def next_page(self):
        if self.current_idx < self.total_pages - 1:
            self.current_idx += 1
        return self
    
    def previous_page(self):
        if self.current_idx > 0:
            self.current_idx -= 1
        return self
    
    def __str__(self):
        visible_items = self.get_visible_items()
        return "\n".join(str(item) for item in visible_items)
    
alphabetList = list("abcdefghijklmnopqrstuvwxyz")
p = Pagination(alphabetList, 4)

print(p.get_visible_items())

p.next_page()
print(p.get_visible_items())

p.last_page()
print(p.get_visible_items())

p.go_to_page(10)
print(p.current_idx + 1)

p.go_to_page(0)
