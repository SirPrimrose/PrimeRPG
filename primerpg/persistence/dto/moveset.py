from typing import List


class Moveset:
    def __init__(self, unique_id: int, move_ids: List[int]):
        self.unique_id = unique_id
        self.move_ids = move_ids
