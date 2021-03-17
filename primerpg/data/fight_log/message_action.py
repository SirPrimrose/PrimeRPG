from primerpg.data.fight_log.action_base import ActionBase


class MessageAction(ActionBase):
    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def get_message(self):
        return self.message
