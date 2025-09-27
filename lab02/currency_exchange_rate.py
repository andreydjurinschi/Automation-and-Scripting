
import argparse
from datetime import datetime

'''
    function that parse the args before script name
'''
def parse_args():
    parser = argparse.ArgumentParser(description="Terminal argument parser")
    parser.add_argument("from", required=True ,help="enter from currency")
    parser.add_argument("to", required=True , help="enter to currency")
    parser.add_argument("date", required=False ,help="enter date YYYY-MM-DD")
    parser.add_argument("key", required=True,help="API key for auth")
    return parser.parse_args()

'''
    function that checks date
'''

def validate_date(date_str, date_format):
    try:
        datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        return False