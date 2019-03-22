#!/usr/bin/env python3

# Libraries
from shutil import copyfile
import argparse
import Table 
import textwrap 


# Arguments parser
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent('''\
    Python Anonymizer - v1.0
    -------------------------------------------------------------------------
      ___                                                 _                  
     / _ \                                               (_)                 
    / /_\ \ _ __    ___   _ __   _   _  _ __ ___   _   _  _  ____  ___  _ __ 
    |  _  || '_ \  / _ \ | '_ \ | | | || '_ ` _ \ | | | || ||_  / / _ \| '__|
    | | | || | | || (_) || | | || |_| || | | | | || |_| || | / / |  __/| |   
    \_| |_/|_| |_| \___/ |_| |_| \__, ||_| |_| |_| \__, ||_|/___| \___||_|   
                                  __/ |             __/ |                    
                                 |___/             |___/        

    -------------------------------------------------------------------------          
    '''))
mutually_group = parser.add_mutually_exclusive_group(required=True)
mutually_group.add_argument('-a', '--anonymize', nargs=2, metavar=('FILENAME', 'OUTPUT'), help='\
    anonymize data from a CSV file and write the output on another file')
mutually_group.add_argument('-c', '--config', action='store_true', help='\
    open a web browser to configure the anonymizer')
mutually_group.add_argument('-s', '--save-config', nargs=1, metavar='FILENAME', help='\
    save anonymizer configuration on a json file')
parser.add_argument('-v', '--version', action='version', version='Python Anonymizer - v1.0')


def main():

    args = parser.parse_args()
    if args.anonymize != None:
        # Anonymize input csv file and export the result 
        pass
    elif args.config:
        # Open web browser to edit the configuration file
        pass
    else:
        # Export the configuration file
        copyfile('.//config//config.json', args.save_config[0])


    '''
    t = Table.Table()

    # Test
    for entry in t.entries:
        entry.print()
    '''
    


if __name__ == '__main__':
    main()