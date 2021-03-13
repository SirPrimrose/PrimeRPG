class MobDrop:
    def __init__(
        self, mob_id: int, item_id: int, drop_rate: float, mean: float, std_dev: float
    ):
        self.mob_id = mob_id
        self.item_id = item_id
        self.drop_rate = drop_rate
        self.mean = mean
        self.std_dev = std_dev
