def test_copy_demo_command(capsys):
    from sorcha.utilities.sorcha_demo_command import print_demo_command

    print_demo_command(printall=True)

    captured = capsys.readouterr()

    expected = (
        "\nThe command to run the Sorcha demo in this version of Sorcha is:\n\n"
        + "\033[1;32;40msorcha -c sorcha_config_demo.ini -p sspp_testset_colours.txt -ob sspp_testset_orbits.des -pd baseline_v2.0_1yr.db -o ./ -t testrun_e2e\033[0m\n\n"
        + "WARNING: This command assumes that the demo files are in your working directory.\n\n"
        + "You can copy the demo files into your working directory by running:\n\n"
        + "\033[1;32;40msorcha_copy_demo_files\033[0m\n\n"
        + "Or, to copy them into a directory of your choice, run:\n\n"
        + "\033[1;32;40msorcha_copy_demo_files -p /path/to/files \033[0m\n\n"
        + "If copying into a directory of your choice, you will need to modify the demo command to path to your files.\n\n"
    )

    assert captured.out == expected
