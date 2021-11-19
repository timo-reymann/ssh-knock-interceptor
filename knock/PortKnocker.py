from config import KnockConfigEntry


class PortKnocker:
    def __init__(self, config_entry: KnockConfigEntry):
        self.config_entry = config_entry

    def print_env(self, var: str, val: str) -> str:
        print(f"export {var}='{val}';")

    def knock(self):
        self.print_env("KNOCK_HOST", self.config_entry.knock_host)
        knock_cmd = f"knock {self.config_entry.knock_host} {self.config_entry.sequence}" \
                    f" -d {self.config_entry.duration}" \
                    f" {'-u' if self.config_entry.use_udp == 'yes' else ''}"
        print(knock_cmd)
