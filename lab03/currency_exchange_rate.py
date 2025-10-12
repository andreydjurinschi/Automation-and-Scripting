import argparse
from datetime import datetime
import requests
import sys
import os
import json


'''
    function that parse the args before script name
'''
def parse_args():
    parser = argparse.ArgumentParser(description="Currency exchange rate script")
    parser.add_argument("--from-currency", required=True, help="Enter source currency (e.g. USD)")
    parser.add_argument("--to-currency", required=True, help="Enter target currency (e.g. EUR)")
    parser.add_argument("--date", required=True, help="Enter date YYYY-MM-DD")
    parser.add_argument("--key", required=True, help="API key for auth")
    return parser.parse_args()


'''
    function that checks date format and range
'''
def validate_date(date_str):
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise argparse.ArgumentTypeError("Incorrect date format. Please use YYYY-MM-DD.")
    
    if not (datetime(2025, 1, 1).date() <= date <= datetime(2025, 9, 15).date()):
        raise ValueError("Date out of range (2025-01-01 .. 2025-09-15).")
    return date


'''
    function that build the url for api request
'''
def fetch_exchange_rate(from_currency, to_currency, date, api_key):
    validate_date(date)
    base_url = f"http://localhost:8080/?from={from_currency}&to={to_currency}&date={date}"

    try:
        response = requests.post(base_url, data={"key": api_key}, timeout=5)
        response.raise_for_status()
        data = response.json()

        if "error" in data and data["error"]:
            raise ValueError(data["error"])

        return data
    except Exception as e:
        log_error(str(e))
        print(f"Error: {e}")
        sys.exit(1)


'''
    function that save the result to a file
'''
def save_result(data, from_cur, to_cur, date):
    os.makedirs("data", exist_ok=True)
    filename = f"data/{from_cur.lower()}_{to_cur.lower()}_{date}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved: {filename}")


'''
    function that logs errors
'''
def log_error(message):
    with open("error.log", "a", encoding="utf-8") as f:
        f.write(message + "\n")

def main():
    args = parse_args()

    from_currency = args.from_currency
    to_currency = args.to_currency
    date = args.date
    api_key = args.key

    data = fetch_exchange_rate(from_currency, to_currency, date, api_key)
    save_result(data, from_currency, to_currency, date)


'''
    entry point
'''
main()
