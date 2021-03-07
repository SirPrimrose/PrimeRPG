idle_state = "idling"
gathering_state = "gathering"
default_start_hp = 100

player_states = enumerate([idle_state, gathering_state])


class PlayerCore:
    def __init__(self, unique_id, name, state, current_hp):
        self.unique_id = unique_id
        self.name = name
        self.state = state
        self.current_hp = current_hp

    def __repr__(self):
        response = "Unique Id: %s" % self.unique_id
        response += "\nName: %s" % self.name
        response += "\nState: %s" % self.state
        response += "\nCurrent HP: %s" % self.current_hp
        return response
