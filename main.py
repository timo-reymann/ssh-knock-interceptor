import sys

from config import KnockConfigFile

ANSI_RED = '\u001b[31;1m'
ANSI_RESET = '\u001b[0m'


def print_err(msg: str):
    print(f"{ANSI_RED}{msg}{ANSI_RESET}")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print_err("Required hostname parameter is missing")
        sys.exit(2)

    config = KnockConfigFile("~/.ssh/knock-config")
    config.parse()
    errors = config.validate()
    if len(errors) > 0:
        print(errors)
        sys.exit(2)

    matches = config.get_matching_entries(sys.argv[1])
    if len(matches) > 1:
        print_err("More than two matches")
        print(matches)
        sys.exit(2)
    elif len(matches) == 0:
        print_err("No match for port knocking")
        sys.exit(1)

    match = matches[0]
    match.create_knocker().knock()
