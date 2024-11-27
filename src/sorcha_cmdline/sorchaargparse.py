import argparse


class SorchaArgparse(argparse.ArgumentParser):

    def __init__(self, *argv, **kwargs):
        super().__init__(**kwargs)

        # rename prog to remove the "-" since on the user will write sorcha verb
        # but we sneakily run as sorcha-verb so that's confusing when the
        # argparse usage or errors print on the terminal. This replacement
        # gets around this so all the usage calls match what the user should
        # be inputting on the command line
        self.prog = self.prog.replace("-", " ")

    def print_usage(self, file=None):
        super().print_usage(file)
        print(f"For more detailed help try: {self.prog} -h ", file=file)
