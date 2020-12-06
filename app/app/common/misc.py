from typing import List
from app.app.common import UrlPullError
from typing import Dict
import datetime
import requests
import json



def _dates(date_count: int = 7) -> List[str]:
    """ Provides list of date strings in yyyy-mm-dd format.
        Dates measured from today until max count.
    """
    return [str(datetime.date.today() + datetime.timedelta(days=offset)) for offset in range(0, date_count)]


def url_pull(url: str, request_headers: Dict[str, str], payload: str) -> str:
    response = requests.post(url=url, data=payload, headers=request_headers)
    if response.status_code != 200:
        raise UrlPullError(f"Unable to pull {url} : {response}")
    return json.loads(response.content)