from configparser import SectionProxy
from pathlib import PurePath
from typing import Union

from knock.PortKnocker import PortKnocker


def err_field_required(field):
    return f"{field} is required"


def must_be_positive_number(field) -> str:
    return f"{field} must be a positive number"


class KnockConfigEntry:
    def __init__(self, host_pattern: str, config_section: Union[dict, SectionProxy]):
        self.host_pattern = host_pattern
        self.knock_host = config_section.get("host", None)
        self.sequence = config_section.get("sequence", None)
        self.duration = config_section.get("duration", 20)
        self.use_udp = config_section.get("udp", "no")

    def validate(self) -> list:
        errors = []

        if self.knock_host is None:
            errors.append(err_field_required("host"))

        if self.sequence is None:
            errors.append(err_field_required("sequence"))

        if self.use_udp not in ["yes", "no"]:
            errors.append("udp must be true/false")

        return errors

    def is_suitable_for_host(self, host: str):
        pattern = PurePath(host)
        return pattern.match(self.host_pattern)

    def create_knocker(self):
        return PortKnocker(self)

    def __str__(self):
        return f"'{self.host_pattern}'[" \
               f"knock_host={self.knock_host}, " \
               f"sequence={self.sequence}," \
               f"duration={self.duration}" \
               f"use_udp={self.use_udp}" \
               f"] "

