idle_state = "idling"
gathering_state = "gathering"

player_states = enumerate([idle_state, gathering_state])


class Player:
    def __init__(self, unique_id, name, state):
        self.unique_id = unique_id
        self.name = name
        self.state = state

    def __repr__(self):
        response = "Unique Id: %s" % self.unique_id
        response += "\nName: %s" % self.name
        response += "\nState: %s" % self.state
        return response
