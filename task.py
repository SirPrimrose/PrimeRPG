class Task:
    def __init__(self, task, time_started):
        self.task = task
        self.time_started = time_started

    def __repr__(self):
        response = 'Unique Id: %s' % self.task
        response += '\nName: %s' % self.time_started
        return response
