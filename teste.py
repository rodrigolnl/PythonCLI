from inspect import signature

from Cli import Cli
from Bag import Bag

def teste():
    print('teste1')


def teste2(text, bag: Bag, cli: Cli):
    print(text)

cli = Cli()

cli.add(function=teste, cmd='teste', group='print')
cli.add(function=teste2, cmd='print')
