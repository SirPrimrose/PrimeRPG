class Task:
    def __init__(self, task, time_started):
        self.task = task
        self.time_started = time_started

    def __repr__(self):
        response = 'Task: %s' % self.task
        response += '\nTime Started: %s' % self.time_started
        return response
