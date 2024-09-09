import os
import sys
import pandas as pd


def find_all_log_files(filepath):
    """Looks for all Sorcha log files in the given filepath and subdirectories
    recursively. Specifically searches for files ending *sorcha.log.

    Parameters
    -----------
    filepath : str
        Filepath of top-level directory within which to search for Sorcha log files.

    Returns
    -----------
    log_files : list
        A list of the discovered log files (absolute paths)

    """
    log_files = []

    for dirpath, dirnames, filenames in os.walk(filepath):
        for filename in [f for f in filenames if f.endswith("sorcha.log")]:
            log_files.append(os.path.join(dirpath, filename))

    return log_files


def check_all_logs(log_files):
    """Checks the last line of all the log files supplied and checks to see
    if the Sorcha run completed successfully, saving the last line of the log
    in question if it did not.

    Parameters
    -----------
    log_files : list
        A list of filepaths pointing to Sorcha log files.

    Returns
    -----------
    good_log : list of Booleans
        A list of whether each log file was deemed to be successful or not

    last_lines : list of str
        A list of the last lines of unsuccessful Sorcha runs.

    """

    good_log = []
    last_lines = []

    for log_file in log_files:
        with open(log_file, "r") as f:
            lines = f.read().splitlines()
            last_line = lines[-1]

            if last_line[-29:] == "Sorcha process is completed. ":
                good_log.append(True)
                last_lines.append(" ")
            else:
                good_log.append(False)
                last_lines.append(last_line)

    return good_log, last_lines


def check_output_logs(filepath, output=False):
    """Searches directories recursively for Sorcha log files, classifies them as
    belonging to successful or unsuccessful Sorcha runs, and provides this information
    to the user. This is helpful in cases where several runs of Sorcha are being
    performed simultaneously (i.e. on a supercomputer). Can output either a .csv
    file or straight to the terminal.

    Parameters
    -----------
    filepath : str
        Filepath of top-level directory within which to search for Sorcha log files.
    output : str or bool
        Either the filepath/name in which to save output, or False to print output to terminal. Default=False.

    """

    log_files = find_all_log_files(filepath)

    if len(log_files) > 0:
        print(str(len(log_files)) + " Sorcha log files have been found. Investigating....\n")
    if len(log_files) == 0:
        sys.exit(
            "ERROR: no Sorcha log files could be found in directories/subdirectories of supplied filepath."
        )

    good_log, last_lines = check_all_logs(log_files)

    log_results = pd.DataFrame(
        {"log_filename": log_files, "run_successful": good_log, "log_lastline": last_lines}
    )
    failed_runs = log_results[~log_results["run_successful"]]

    if len(failed_runs) > 0:
        print(str(len(failed_runs)) + " unsuccessful Sorcha run(s) found.\n")

        if output:
            print("Saving results to: " + output)
            log_results.to_csv(os.path.join(output), index=False)
        else:
            for i, row in failed_runs.iterrows():
                print("Failed run log filename:\n\t" + row["log_filename"])
                print("Failed run last line of log:\n\t" + row["log_lastline"])
                print("\n")

    else:
        print("All Sorcha runs appear to have completed successfully. :)")
        if output:
            print("No output will be saved.")

    return
