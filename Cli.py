import time
from inspect import isfunction
import re
from Bag import Bag
from Command import Command
import threading


class Cli:
    def __init__(self):
        self.list_commands: list[Command] = []
        self._loop_bot_flag = True
        self._loop_bot_thread = None
        self._start_loop_bot()

        self._cli_reading_bot_flag = True
        self._cli_reading_bot_thread = None
        self._start_cli_reading_bot()

    def add(self, function, cmd, args=None, nickname: str = '',
            begin: bool = False, loop: bool = False,  bag: Bag = Bag(), group: str = 'Main'):
        self.list_commands.append(Command(function, cmd, args, nickname, begin, loop, bag, group))
        if begin:
            self.list_commands[-1].run(args)

    def get_command(self, id, group='Main'):
        if isfunction(id):
            for command in self.list_commands:
                if command.function == id:
                    return command
        elif type(id) is str:
            for command in self.list_commands:
                if command.cmd == id and command.group == group:
                    return command
            for command in self.list_commands :
                if command.nickname == id and command.group == group:
                    return command
        elif type(id) is int :
            return self.list_commands[int]

    def _start_loop_bot(self):
        self._loop_bot_thread = threading.Thread(target=self._loop_bot)
        self._loop_bot_thread.start()

    def _loop_bot(self):
        while self._loop_bot_flag:
            for command in self.list_commands:
                if command.loop:
                    command.run(command.args)
            time.sleep(0.01)

    def _start_cli_reading_bot(self):
        self._cli_reading_bot_thread = threading.Thread(target=self._cli_reading_bot)
        self._cli_reading_bot_thread.start()

    def _cli_reading_bot(self):
        while self._cli_reading_bot_flag:
            cmd_input = input('>')
            list_text = []
            while re.search('\".*?\"', cmd_input):
                list_text.append(re.search('\".*?\"', cmd_input).group().replace('\"', ''))
                cmd_input = re.sub('\".*?\"', '#text', cmd_input)
            entries = [entry.replace('#text', list_text.pop(0) if list_text else '') for entry in cmd_input.split(' ')]

            if entries[0] in [cmd.group for cmd in self.list_commands]:
                if len(entries) > 1 and entries[1] in [cmd.cmd for cmd in self.list_commands]:
                    args = tuple(entries[2:len(entries)])
                    self.get_command(entries[1], entries[0]).run(args)
                elif entries[0] in [cmd.cmd for cmd in self.list_commands]:
                    args = tuple(entries[1:len(entries)])
                    self.get_command(entries[0]).run(args)

            elif entries[0] in [cmd.cmd for cmd in self.list_commands]:
                args = tuple(entries[1:len(entries)])
                self.get_command(entries[0]).run(args)

            else:
                pass
