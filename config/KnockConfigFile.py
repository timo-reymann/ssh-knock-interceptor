from configparser import ConfigParser
from os.path import expanduser

from config import KnockConfigEntry


class KnockConfigFile:
    def __init__(self, path):
        self.path = expanduser(path)
        self.config = ConfigParser()
        self.entries: list = []

    def parse(self):
        self.config.read(self.path, 'utf8')
        for section in self.config.sections():
            self.entries.append(KnockConfigEntry(section, self.config[section]))

    def validate(self):
        errors = []

        for entry in self.entries:
            errors = entry.validate()
            if len(errors) > 0:
                errors.append((entry.host_pattern, errors))

        return errors

    def get_matching_entries(self, hostname):
        matches = []
        for entry in self.entries:
            if entry.is_suitable_for_host(hostname):
                matches.append(entry)
        return matches
