from typing import List


class ItemMoveset:
    def __init__(self, item_id: int, moveset_ids: List[int]):
        self.item_id = item_id
        self.moveset_ids = moveset_ids
