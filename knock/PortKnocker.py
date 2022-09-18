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
        ports = self.config_entry.sequence.split(" ")
        last_index = len(ports) - 1
        for i, port in enumerate(ports):
            use_udp = self.config_entry.use_udp == "yes"
            if port.find(':') != -1:
                port, protocol = port.split(':', 2)
                if protocol == 'tcp':
                    use_udp = False
                elif protocol == 'udp':
                    use_udp = True
                else:
                    error = 'Invalid protocol "{}" given. Allowed values are "tcp" and "udp".'
                    raise ValueError(error.format(protocol))


            # print('hitting %s %s:%d' % ('udp' if use_udp else 'tcp', self.config_entry.knock_host, int(port)))

            s = socket.socket(self.address_family, socket.SOCK_DGRAM if use_udp else socket.SOCK_STREAM)
            s.setblocking(False)

            socket_address = (self.config_entry.knock_host, int(port))
            if use_udp:
                s.sendto(b'', socket_address)
            else:
                s.connect_ex(socket_address)
                select.select([s], [s], [s], 1)

            s.close()

            if self.config_entry.duration and i != last_index:
                time.sleep(self.config_entry.duration / 1000)

        self.print_env("KNOCK_HOST", self.config_entry.knock_host)
