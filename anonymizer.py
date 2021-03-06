#!/usr/bin/env python3

# Libraries
from modules import *
from config import configurator
from shutil import copyfile
import argparse
import textwrap


# Arguments parser
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description=textwrap.dedent('''\
    Python Anonymizer - v1.0
    -------------------------------------------------------------------------
      ___                                          _                  
     / _ \                                        (_)                 
    / /_\ \ _ __    ___   _ __   _   _  _ __ ___   _  ____  ___  _ __ 
    |  _  || '_ \  / _ \ | '_ \ | | | || '_ ` _ \ | ||_  / / _ \| '__|
    | | | || | | || (_) || | | || |_| || | | | | || | / / |  __/| |   
    \_| |_/|_| |_| \___/ |_| |_| \__, ||_| |_| |_||_|/___| \___||_|   
                                  __/ |                               
                                 |___/                                

    -------------------------------------------------------------------------          
    '''))
mutually_group = parser.add_mutually_exclusive_group(required=True)
mutually_group.add_argument('-a', '--anonymize', nargs=2, metavar=('FILENAME', 'OUTPUT'), help='\
    anonymize data from a CSV file and write the output on another file')
mutually_group.add_argument('-c', '--config', action='store_true', help='\
    open a web browser to configure the anonymizer')
mutually_group.add_argument('-s', '--save-config', nargs=1, metavar='FILENAME', help='\
    save anonymizer configuration on a json file')
parser.add_argument('-v', '--version', action='version',
                    version='Python Anonymizer - v1.0')


def main():
    args = parser.parse_args()

    try:
        if args.anonymize != None:
            # Anonymize input csv file and export the result
            t = Table.Table(args.anonymize[0], args.anonymize[1])
            t.start()
            print("Your file has been anonymized!")

        elif args.config:
            # Open web browser to edit the configuration file
            print("This feature has not been implemented yet! Sorry")
            pass
            
        else:
            # Export the configuration file
            copyfile('./config/config.json', args.save_config[0])
            print("Configuration file has been exported!")

    except Exception as e:
        print("Fatal error! ", e)
    finally:
        print("Program terminated! Goodbye.\n")


if __name__ == '__main__':
    main()
