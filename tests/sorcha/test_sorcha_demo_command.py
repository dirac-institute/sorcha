def test_copy_demo_command(capsys):
    from sorcha.utilities.sorcha_demo_command import print_demo_command, get_demo_command

    print_demo_command(printall=True)
    current_demo_command = get_demo_command()

    captured = capsys.readouterr()

    expected = f"""
The command to run the Sorcha demo in this version of Sorcha is:

    [1;32;40m{current_demo_command}[0m

WARNING: This command assumes that the demo files are in your working directory.

You can copy the demo files into your working directory by running:

    [1;32;40msorcha demo prepare[0m

Or, to copy them into a directory of your choice, run:

    [1;32;40msorcha demo prepare -p /path/to/files [0m

If copying into a directory of your choice, you will need to modify the demo command to path to your files.

"""

    assert captured.out == expected
