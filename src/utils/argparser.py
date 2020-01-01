from argparse import ArgumentParser


class KontArgumentParser(object):
    def __init__(self):

        self.parser = ArgumentParser()
        self.parser.add_argument('-v',
                                 '--verbose',
                                 help='increase output verbosity',
                                 action='store_true')
        self.parser.add_argument('-c',
                                 '--config',
                                 default='config.ini',
                                 help='path to config.ini',
                                 type=str)
        self.args = self.parser.parse_args()

    def get_args(self):
        return self.args
