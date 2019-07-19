from typing import Set

from django.utils.functional import cached_property
from returns import returns


class Plugins:
    FILENAME = 'flake8-extensions.txt'

    def __init__(self, filename=FILENAME):
        self.filename = filename

    @cached_property
    @returns(set)
    def plugins(self) -> Set[str]:
        with open(self.filename) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                yield line

    def add(self, plugin: str):
        self.plugins.add(plugin)

    def __iter__(self):
        return iter(sorted(self.plugins))

    def update(self):
        with open(self.filename, mode='w') as f:
            for plugin in self:
                f.write(plugin)
                f.write('\n')


def main():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('plugin', nargs='+')
    args = parser.parse_args()

    plugins = Plugins()
    for plugin in args.plugin:
        plugins.add(plugin)
    plugins.update()
    print("Don't forget to run `pip install -e .[dev]` to update")


if __name__ == '__main__':
    main()
