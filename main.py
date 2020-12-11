# Main entry point
from app.app.observer import ETCCWatcher
from app.app.common.misc import future_dates

etcc_watcher = ETCCWatcher()

for date in future_dates(5):
    for args in etcc_watcher.retrieve_for_date(date):
        print(args)

