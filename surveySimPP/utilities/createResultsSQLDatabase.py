# This script will conjoin SSPP results (if saved as SQL databases) and inputs
# (physical parameters, orbits, cometary info, etc) into one SQL database with
# tables SSPP_results, physical_parameters, orbits, cometary_parameters (if used)

# The code assumes that your physical/cometary parameters and orbits files are
# in the same folder and begin with 'colours', 'comet' and 'orbits' respectively.
# It also assumes that they are whitespace-separated. Feel free to adapt for your
# own use-case :)

import pandas as pd
import sqlite3
import glob
import argparse
import sys
from surveySimPP.modules.PPConfigParser import PPFindDirectoryOrExit


def create_results_table(cnx_out, output_path, output_stem, table_name='pp_results'):

    output_list = glob.glob(output_path + '/**/' + output_stem + '*.db', recursive=True)

    if not output_list:
        sys.exit('Could not find any .db files using given filepath and stem.')

    column_names = get_column_names(output_list[0])

    cur_out = cnx_out.cursor()
    cur_out.execute('DROP TABLE if exists ' + table_name)

    # the below ensures that column names with parentheses don't confuse SQL
    column_string = '[' + '], ['.join(column_names) + ']'

    create_command = 'CREATE TABLE ' + table_name + '(' + column_string + ')'

    cur_out.execute(create_command)

    # building the correct SQL command to add data
    questions = '(' + (len(column_names) - 1) * '?, ' + '?)'
    sql_command = 'INSERT into ' + table_name + ' VALUES ' + questions

    for filename in output_list:
        con = sqlite3.connect(filename)
        cur = con.cursor()

        cur.execute('SELECT * FROM pp_results')
        output = cur.fetchall()

        for row in output:
            cur_out.execute(sql_command, row)

        cur.close()

    cur_out.close()
    cnx_out.commit()


def create_inputs_table(cnx_out, input_path, table_type):

    input_list = glob.glob(input_path + '/' + table_type + '*', recursive=True)

    if not input_list:
        sys.exit('Could not find any ' + table_type + ' files in given inputs folder.')

    cur_out = cnx_out.cursor()
    cur_out.execute('DROP TABLE if exists ' + table_type)

    for filename in input_list:
        df = pd.read_csv(filename, sep=' ')
        df.to_sql(table_type, cnx_out, if_exists='append')

    cur_out.close()


def create_results_database(args):

    cnx_out = sqlite3.connect(args.filename)

    create_results_table(cnx_out, args.outputs, args.stem)

    create_inputs_table(cnx_out, args.inputs, 'params')
    create_inputs_table(cnx_out, args.inputs, 'orbits')

    if args.comet:
        create_inputs_table(cnx_out, 'comet')


def get_column_names(filename, table_name='pp_results'):

    con_col = sqlite3.connect(filename)
    cur_col = con_col.cursor()
    cur_col.execute('SELECT * from ' + table_name)
    col_names = list(map(lambda x: x[0], cur_col.description))
    cur_col.close()

    return col_names


def main():

    parser = argparse.ArgumentParser(description='Creating a combined results+inputs SQL database.')

    # filepath/name to save script as
    parser.add_argument('-f', '--filename', help='Filepath and name where you want to save the database.', type=str, required=True)
    # path to inputs
    parser.add_argument('-i', '--inputs', help='Path location of input text files (orbits, colours and config files).', type=str, required=True)
    # path to outputs
    parser.add_argument('-o', '--outputs', help='Path location of SSPP output files/folders. Code will search subdirectories recursively.', type=str, required=True)
    # stem filename for outputs
    parser.add_argument('-s', '--stem', help='Stem filename of outputs. Used to find output filenames.', type=str, required=True)
    # include cometary?
    parser.add_argument('-c', '--comet', help='Toggle whether to look for cometary activity files. Default False.', default=False, action='store_true')

    args = parser.parse_args()

    _ = PPFindDirectoryOrExit(args.inputs, '-i, --inputs')
    _ = PPFindDirectoryOrExit(args.outputs, '-o, --outputs')

    create_results_database(args)


if __name__ == '__main__':
    main()
