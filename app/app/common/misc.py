from typing import List
from app.app.common import UrlPullError
from bs4 import BeautifulSoup as BS
from typing import Dict
import datetime
import requests
import json
import re


def parse_html_table(html_string: str, regex: str) -> List[tuple]:
    html_to_table = []
    soup = BS(html_string, 'lxml')
    for row in soup.find_all("tr"):
        html_to_table.append(re.findall(regex, str(row)))
        print(row)
    return html_to_table


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
