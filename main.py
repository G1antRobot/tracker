#!/usr/env python3
# Main entry point
from app.observer import ETCCWatcher
from app.common.misc import future_dates
import os
import requests
import json

GW_SERVER = os.environ['API_GW']
GW_PORT = os.environ['API_GW_PORT']
URL = f'http://{GW_SERVER}:{GW_PORT}/'
UPDATE_SLOT_URL = f'{URL}update_slot'
HEADERS = {'Content-type': 'application/json'}


def main():
    # GW_SERVER = os.environ['GW_ADDRESS']
    # GW_PORT = os.environ['GW_PORT']
    etcc_watcher = ETCCWatcher()
    for date in future_dates(14):
        print(f"Posting database for {date}!")
        for _, month_, date_, slot_name, slot_free_count in etcc_watcher.retrieve_for_date(date):
            data = {"month": month_, "date": date_, "slot_name": slot_name, "slot_free_count": slot_free_count}
            requests.post(UPDATE_SLOT_URL, data=json.dumps(data), headers=HEADERS)


if __name__ == "__main__":
    main()
