#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm


class PersistenceException(Exception):
    def __init__(self, object_type: type):
        self.object_type = object_type

    def __str__(self):
        return "Failed to define {} from database row.".format(self.object_type.__name__)
