#!/usr/env python3
# Main entry point
from app.observer import ETCCWatcher
from app.common.misc import future_dates
from time import sleep
import os
import requests
import json

GW_SERVER = os.environ['API_GW']
GW_PORT = os.environ['API_GW_PORT']
BREAK_TIME = os.environ.get('SLEEP_TIME', 2)
DAYS_TO_WATCH = os.environ.get('DAYS', 7)
#
URL = f'http://{GW_SERVER}:{GW_PORT}'
UPDATE_SLOT_URL = f'{URL}/update_slot'
HEADERS = {'Content-type': 'application/json'}


def retrieve_date_info(watcher_obj: ETCCWatcher, date:str) -> dict:
    for _, month_, date_, slot_name, slot_free_count in watcher_obj.retrieve_for_date(date):
        yield {"month": month_, "date": date_, "slot_name": slot_name, "slot_free_count": slot_free_count}


def update_db(data: dict) -> None:
    requests.post(UPDATE_SLOT_URL, data=json.dumps(data), headers=HEADERS)


def main():
    etcc_watcher = ETCCWatcher()
    print(f"Starting Tracker - days to watch {DAYS_TO_WATCH} , wait time {BREAK_TIME}s")
    while True:
        for date in future_dates(DAYS_TO_WATCH):
            for data in retrieve_date_info(etcc_watcher, date):
                update_db(data)
            print(f"Posting database for {date}!")
        sleep(BREAK_TIME)


if __name__ == "__main__":
    main()
