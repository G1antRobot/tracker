#!/usr/env python3
# Main entry point

from app.observer import ETCCWatcher
from app.common.misc import future_dates


def main():
    etcc_watcher = ETCCWatcher()

    for date in future_dates(5):
        for args in etcc_watcher.retrieve_for_date(date):
            print(args)


if __name__ == "__main__":
   main()
