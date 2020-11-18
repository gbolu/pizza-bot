def parse_command(command: str, last_command: str):
    if command == 'pizza':
        if last_command != '':
            res