from abc import abstractmethod


class ActionBase:
    def __init__(self):
        pass

    @abstractmethod
    def get_message(self):
        pass
