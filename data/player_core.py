idle_state = "idling"
gathering_state = "gathering"
default_start_hp = 100

player_states = enumerate([idle_state, gathering_state])


class PlayerCore:
    def __init__(
        self, unique_id: int, name: str, avatar_url: str, state: str, current_hp: int
    ):
        self.unique_id = unique_id
        self.name = name
        self.avatar_url = avatar_url
        # TODO Update state to state_id
        self.state = state
        self.current_hp = current_hp

    def __repr__(self):
        response = "Unique Id: %s" % self.unique_id
        response += "\nName: %s" % self.name
        response += "\nAvatar URL: %s" % self.avatar_url
        response += "\nState: %s" % self.state
        response += "\nCurrent HP: %s" % self.current_hp
        return response
