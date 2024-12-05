from argparse import ArgumentParser


class SorchaArgumentParser(ArgumentParser):
    """A subclass of the argparse.ArgumentParser that adds in a print statement
    to make it clearer how to get detailed help for new users who may not be
    as familiar with linux/unix"""

    def __init__(self, *args, **kwargs):
        """A subclass of the argparse.ArgumentParser that adds in a print statement
        to make it clearer how to get detailed help for new users who may not be
        as familiar with linux/unix

        Parameters
        -----------
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)

    def print_usage(self, file=None):
        """Print a brief description of how the ArgumentParser should be invoked
        on the command line. If file is None, sys.stdout is assumed.


        Parameters
        -----------
        file: str or None
            Variable length argument list.

        Returns
        -----------
        None.

        """
        super().print_usage(file)
        print(f"For more detailed help try: {self.prog} -h ", file=file)
