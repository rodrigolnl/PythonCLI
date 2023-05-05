from inspect import signature
from Bag import Bag
import threading
import Cli

class Command:
    def __init__(self, function, cmd, args=None, nickname: str = '',
                 begin: bool = False, loop: bool = False, bag: Bag = Bag(), group: str = None):
        self.function = function
        self.nickname = nickname
        self.cmd = cmd
        self.args = args
        self.begin = begin
        self.loop = loop
        self.bag = bag
        self.thread = None
        self.group = group

    def run(self, args):
        new_args = ()
        i = 0
        for parameter in signature(self.function).parameters:
            if parameter.lower() == 'bag':
                new_args = new_args + (self.bag,)
            elif parameter.lower() == 'cli':
                new_args = new_args + (self,)
            else:
                new_args = new_args + (args[i],)
                i += 1
        if self.thread is None:
            self.thread = threading.Thread(target=self.function, args=new_args)
            self.thread.start()
        elif not self.thread.is_alive():
            self.thread = threading.Thread(target=self.function, args=new_args)
            self.thread.start()
