def test_copy_demo_command(capsys):
    from sorcha.utilities.sorcha_demo_command import print_demo_command, get_demo_command

    print_demo_command(printall=True)
    current_demo_command = get_demo_command()

    captured = capsys.readouterr()

    expected = (
        "\nThe command to run the Sorcha demo in this version of Sorcha is:\n\n"
        + "\033[1;32;40m"
        + current_demo_command
        + "\033[0m\n\n"
        + "WARNING: This command assumes that the demo files are in your working directory.\n\n"
        + "You can copy the demo files into your working directory by running:\n\n"
        + "\033[1;32;40msorcha_copy_demo_files\033[0m\n\n"
        + "Or, to copy them into a directory of your choice, run:\n\n"
        + "\033[1;32;40msorcha_copy_demo_files -p /path/to/files \033[0m\n\n"
        + "If copying into a directory of your choice, you will need to modify the demo command to path to your files.\n\n"
    )

    assert captured.out == expected
