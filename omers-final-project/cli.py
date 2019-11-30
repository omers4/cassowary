import functools
import inspect
import sys

USAGE_MSG = 'USAGE: python example.py <command> [<key>=<value>]*'
USAGE_BAD_COMMAND_MSG = f'Command not found. {USAGE_MSG}'
USAGE_BAD_PARAM_MSG = f'Bad param format. {USAGE_MSG}'
USAGE_INVALID_PARAM_MSG = f'Invalid param. {USAGE_MSG}'


class CommandLineInterface:

    def __init__(self):
        self._commands = {}

    def command(self, f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            f(*args, **kwargs)
        self._commands[f.__name__] = f
        return wrapper

    def main(self):
        if not sys.argv or len(sys.argv) < 2:
            print(USAGE_MSG)
            exit(1)

        exec, command_name, *raw_params = sys.argv
        params = [param.split('=') for param in raw_params]

        command = self._commands.get(command_name)

        if command is None:
            print(USAGE_BAD_COMMAND_MSG)
            exit(1)

        call_args = inspect.getfullargspec(command)
        for param in params:
            if len(param) != 2:
                print(USAGE_BAD_PARAM_MSG)
                exit(1)
            key, val = param
            if key not in call_args.args:
                print(USAGE_INVALID_PARAM_MSG)
                exit(1)

        params_dict = {key: value for key, value in params}
        self._commands[command_name](**params_dict)
        sys.exit(0)
