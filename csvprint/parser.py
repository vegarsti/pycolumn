import argparse
import sys
import csv
from itertools import islice
from .parse_types import *

def create():
    script_name = 'csvprint'
    parser = argparse.ArgumentParser(
        description='Command line utility for pretty printing csv files.',
        formatter_class=argparse.RawTextHelpFormatter,
        prog=script_name,
    )
    parser.add_argument(
        'filename',
        type=str,
        help='file to pretty print',
        nargs='?',
    )
    parser.add_argument(
        '-s',
        '--separator',
        default=',',
        help="separator/delimiter used in csv file\ndefault is comma\nuse 'tab' for tab separated files\n",
        type=separator,
    )
    parser.add_argument(
        '-n',
        '--rows',
        type=positive_integer,
        default=sys.maxsize,
        help='number of rows to show',
    )
    parser.add_argument(
        '-j',
        '--justify',
        nargs='+',
        default=['<'],
        help='which justification to use\ndefault is left\nchoices: {l, r}\n'
            + 'can provide a list, in which case\none choice for each column',
        type=justification,
    )
    parser.add_argument(
        '-d',
        '--decorator',
        type=str,
        default='',
        help='which string/decorator to use in spacing',
    )
    parser.add_argument(
        '-p',
        '--padding',
        type=non_negative_integer,
        default=1,
        help='padding',
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--header',
        action='store_true',
        help='header decoration',
    )
    group.add_argument(
        '--markdown',
        action='store_true',
        help='output markdown table',
    )
    return parser

def print_message_and_exit(parser, message):
    script_name = 'csvprint'
    parser.print_usage()
    print("{}: error:".format(script_name), end=' ')
    print(message)
    sys.exit()

def file_error_checking(parser, args):
    reading_from_pipe = not sys.stdin.isatty() and args['filename'] == None
    if reading_from_pipe:
        args['csvfile'] = sys.stdin
    elif args['filename'] == None:
        print_message_and_exit(
            parser,
            "required: filename or pipe",
        )
    else:
        try:
            args['csvfile'] = open(args['filename'])
        except FileNotFoundError:
            print_message_and_exit(parser, "no such file: {}".format(args['filename']))

def check_errors(parser, args):
    file_error_checking(parser, args)
    return args

def parse_cli_arguments(parser):
    args = vars(parser.parse_args())
    args = check_errors(parser, args)
    if args['markdown']:
        args['decorator'] = '|'
    return args

def store_content(parser, args):
    csvreader = csv.reader(args['csvfile'], delimiter=args['separator'])
    header = next(csvreader)
    args['num_columns'] = len(header)
    justify_all_columns_equally = len(args['justify']) == 1
    justification_and_columns_differ = len(args['justify']) != args['num_columns']
    if justify_all_columns_equally:
        args['justify'] = [args['justify'][0]] * args['num_columns']
    elif justification_and_columns_differ:
        print_message_and_exit(
            parser,
            'argument -j/--justify: only one argument or one per column'
        )
    args['content'] = [header]
    row_number = 0
    for row_number, row in enumerate(islice(csvreader, args['rows'] - 1)):
        args['content'].append(row)
    args['rows'] = row_number + 1