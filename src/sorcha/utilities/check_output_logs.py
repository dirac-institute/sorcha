import os
import pandas as pd


def find_all_log_files(filepath):
    log_files = []

    for dirpath, dirnames, filenames in os.walk(filepath):
        for filename in [f for f in filenames if f.endswith(".log")]:
            log_files.append(os.path.join(dirpath, filename))

    return log_files


def check_all_logs(log_files):
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


def check_output_logs(filepath, output):
    log_files = find_all_log_files(filepath)

    if len(log_files) > 0:
        print(str(len(log_files)) + " Sorcha log files have been found. Investigating....\n")
    if len(log_files) == 0:
        print("No Sorcha log files could be found in directories/subdirectories of supplied filepath.")
        return

    good_log, last_lines = check_all_logs(log_files)

    log_results = pd.DataFrame(
        {"log_filename": log_files, "run_successful": good_log, "log_lastline": last_lines}
    )
    failed_runs = log_results[~log_results["run_successful"]]

    if len(failed_runs) > 0:
        print(str(len(failed_runs)) + " unsuccessful Sorcha run(s) found.\n")

        if output:
            print("Saving results to: " + output)
            log_results.to_csv(os.path.join(output))
        else:
            for i, row in failed_runs.iterrows():
                print("Failed run log filename:\n\t" + row["log_filename"])
                print("Failed run last line of log:\n\t" + row["log_lastline"])
                print("\n\n")

    else:
        print("All Sorcha runs appear to have completed successfully. :)")

    return
