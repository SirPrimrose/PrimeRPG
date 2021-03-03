from abc import abstractmethod


class Command:
    @abstractmethod
    def get_description(self):
        pass

    @abstractmethod
    def get_name(self):
        pass

    # Always use lowercase characters for prefixes
    @abstractmethod
    def get_prefixes(self):
        pass

    @abstractmethod
    def run_command(self, msg, args):
        pass
