# This script will conjoin SSPP results (if saved as SQL databases) and inputs
# (physical parameters, orbits, cometary info, etc) into one SQL database with
# tables SSPP_results, physical_parameters, orbits, cometary_parameters (if used)

# The code assumes that your physical/cometary parameters and orbits files are
# in the same folder and begin with 'params', 'comet' and 'orbits' respectively.
# It also assumes that they are whitespace-separated. Feel free to adapt for your
# own use-case :)

import pandas as pd
import sqlite3
import glob
import argparse
import sys
import os


def create_results_table(cnx_out, filename, output_path, output_stem, table_name="sorcha_results"):
    """
    Creates a table in a SQLite database from SSPP results.

    Parameters
    -----------
    cnx_out : sqlite3 connection
        Connection to sqlite3 database.

    filename : string
        filepath/name of sqlite3 database.

    output_path : string
        filepath of directory containing SSPP output folders.

    output_stem : string
        stem filename for SSPP outputs.

    table_name : string, optional
        name of table of for storing sorcha results. Default ="sorcha_results"

    Returns
    -----------
    None

    """

    output_list = glob.glob(os.path.join(output_path, "**", output_stem + "*.db"), recursive=True)

    if filename in output_list:
        output_list.remove(filename)

    if not output_list:
        sys.exit("Could not find any .db files using given filepath and stem.")

    column_names = get_column_names(output_list[0])

    cur_out = cnx_out.cursor()
    cur_out.execute("DROP TABLE if exists " + table_name)

    # the below ensures that column names with parentheses don't confuse SQL
    column_string = "[" + "], [".join(column_names) + "]"

    create_command = "CREATE TABLE " + table_name + "(" + column_string + ")"

    cur_out.execute(create_command)

    # building the correct SQL command to add data
    questions = "(" + (len(column_names) - 1) * "?, " + "?)"
    sql_command = "INSERT into " + table_name + " VALUES " + questions

    for filename in output_list:
        con = sqlite3.connect(filename)
        cur = con.cursor()

        cur.execute("SELECT * FROM sorcha_results")
        output = cur.fetchall()

        for row in output:
            cur_out.execute(sql_command, row)

        cur.close()

    cur_out.close()
    cnx_out.commit()


def create_inputs_table(cnx_out, input_path, table_type):
    """
    Creates a table in a SQLite database from the input files (i.e. orbits,
    physical parameters, etc).

    Parameters
    -----------
    cnx_out : sqlite3 connection
        Connection to sqlite3 database.

    input_path : string
        Filepath of directory containing input files.

    table_type : string
        Type of file. Should be "orbits"/"params"/"comet".

    Returns
    -----------
    None

    """

    input_list = glob.glob(input_path + "/" + table_type + "*", recursive=True)

    if not input_list:
        sys.exit("Could not find any " + table_type + " files in given inputs folder.")

    cur_out = cnx_out.cursor()
    cur_out.execute("DROP TABLE if exists " + table_type)

    for filename in input_list:
        df = pd.read_csv(filename, sep="\\s+")

        if "INDEX" in df.columns:
            df = df.rename(columns={"INDEX": "orig_index"})

        df.to_sql(table_type, cnx_out, if_exists="append")

    cur_out.close()


def create_results_database(args):
    """
    Creates a SQLite database with tables of SSPP results and all orbit/physical
    parameters/comet files.

    Parameters
    -----------
    args : ArgumentParser
        argparse ArgumentParser object; command line arguments.

    Returns
    -----------
    None

    """

    cnx_out = sqlite3.connect(args.filename)

    if args.stem:
        stemname = args.stem
    else:
        stemname = ""

    create_results_table(cnx_out, args.filename, args.outputs, stemname)

    create_inputs_table(cnx_out, args.inputs, "params")
    create_inputs_table(cnx_out, args.inputs, "orbits")

    if args.comet:
        create_inputs_table(cnx_out, "comet")


def get_column_names(filename, table_name="sorcha_results"):
    """
    Obtains column names from a table in a SQLite database.

    Parameters
    -----------
    filename : string
        Filepath/name of sqlite3 database.

    table_name : string, optional
        Name of table. Default = "sorcha_results"

    Returns
    -----------
    col_names (list): list of column names.

    """

    con_col = sqlite3.connect(filename)
    cur_col = con_col.cursor()
    cur_col.execute("SELECT * from " + table_name)
    col_names = list(map(lambda x: x[0], cur_col.description))
    cur_col.close()

    return col_names
