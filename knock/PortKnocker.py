import socket
import select
import time
from config import KnockConfigEntry

class PortKnocker:
    def __init__(self, config_entry: KnockConfigEntry):
        self.config_entry = config_entry
        self.address_family, _, _, _, ip = socket.getaddrinfo(
            host=self.config_entry.knock_host,
            port=None,
            flags=socket.AI_ADDRCONFIG
        )[0]
        self.ip_address = ip[0]

    def print_env(self, var: str, val: str) -> str:
        print(f"export {var}='{val}';")

    def knock(self):
        last_index = len(self.config_entry.sequence) - 1
        for i, port in enumerate(self.config_entry.sequence):
            use_udp = self.config_entry.use_udp
            if port.find(':') != -1:
                port, protocol = port.split(':', 2)
                if protocol == 'tcp':
                    use_udp = False
                elif protocol == 'udp':
                    use_udp = True
                else:
                    error = 'Invalid protocol "{}" given. Allowed values are "tcp" and "udp".'
                    raise ValueError(error.format(protocol))


            print('hitting %s %s:%d' % ('udp' if use_udp else 'tcp', self.ip_address, int(port)))

            s = socket.socket(self.address_family, socket.SOCK_DGRAM if use_udp else socket.SOCK_STREAM)
            s.setblocking(False)

            socket_address = (self.ip_address, int(port))
            if use_udp:
                s.sendto(b'', socket_address)
            else:
                s.connect_ex(socket_address)
                select.select([s], [s], [s], self.config_entry.duration)

            s.close()

            if self.config_entry.duration and i != last_index:
                time.sleep(self.config_entry.duration)

        self.print_env("KNOCK_HOST", self.config_entry.knock_host)
        knock_cmd = f"knock {self.config_entry.knock_host} {self.config_entry.sequence}" \
                    f" -d {self.config_entry.duration}" \
                    f" {'-u' if self.config_entry.use_udp == 'yes' else ''}"
        print(knock_cmd)
