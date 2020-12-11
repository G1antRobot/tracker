from app.observer.watcher import Watcher
from typing import Tuple, Iterable
from app.common import url_pull, parse_html_table


class ETWatcher(Watcher):
    _gym_name = ''
    _base_url = ''
    _et_headers = {}
    _payload = ''
    _database_connection = None

    def _get_payload(self, date_info: str) -> str:
        return self._payload.format(date_info)

    def retrieve(self, date_info: str) -> str:
        formatted_payload = self._get_payload(date_info)
        pulled_data = url_pull(self._base_url,
                               payload=formatted_payload,
                               request_headers=self._et_headers)
        return pulled_data['event_list_html']

    @staticmethod
    def _format_parsed(day_of_week, month, day, time_slot, count) -> Tuple:
        if count == 'offering-page-event-is-full':
            f_count = 0
        else:
            try:
                f_count = int(count)
            except Exception as e:
                raise RuntimeError(f"Unexpected count data {count} : error {repr(e)}")

        f_time_slot = "_".join([x.lower() for x in time_slot.split() if x])
        return day_of_week.lower(), month.lower(), day.lower(), f_time_slot.lower(), f_count

    @staticmethod
    def _extract_schedule_info(html_data):
        regex1 = r'''([M,T,W,F,S][a-z]{2}),\s+([A-Z][a-z]+)\s(\d+),\s([0-9:]+ [A-Z]+\s+to\s+[0-9:]+ [A-Z]+)\n</td>\n<td>\n<strong>Availability</strong><br/>(\d+)\s+spaces'''
        regex2 = r'''([M,T,W,F,S][a-z]{2}),\s+([A-Z][a-z]+)\s(\d+),\s([0-9:]+ [A-Z]+\s+to\s+[0-9:]+ [A-Z]+)\n</td>\n<td>\n<strong>Availability</strong><br/><div class="(offering-page-event-is-full)'''
        data = parse_html_table(html_data, regex1)
        data1 = parse_html_table(html_data, regex2)
        d = data+data1
        return [d for d in data+data1 if d]

    def retrieve_for_date(self, date_: str) -> Iterable:
        for record in self._extract_schedule_info(self.retrieve(date_)):
            yield self._format_parsed(*record)

    def update_database(self) -> None:
        pass


class ETCCWatcher(ETWatcher):
    _gym_name = "ETCC"
    _base_url = 'https://app.rockgympro.com/b/widget/?a=equery'
    _et_headers = {
        'Host': 'app2.rockgympro.com',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'en-us',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://app.rockgympro.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/87.0.4280.67 Safari/537.36',
        'Connection': 'keep-alive',
        'Referer': 'https://app.rockgympro.com/b/widget/?a=offering&offering_guid=2923df3b2bfd4c3bb16b14795c569270&'
                   'random=5fbf48c67e946&iframeid=&mode=p',
        'Content-Length': '1550',
        'Cookie': 'AWSELB=A5EDC1071EB54DEE085FA9BC53DB5910EF75B9C87F1017073E8B0D71F097020F81072E969926CF7FF56E9A38BD28D'
                  'D45BF4041CDE064EAF6E07C2B6B89192D65362084B355; AWSELBCORS=A5EDC1071EB54DEE085FA9BC53DB5910EF75B9C87F'
                  '1017073E8B0D71F097020F81072E969926CF7FF56E9A38BD28DD45BF4041CDE064EAF6E07C2B6B89192D65362084B355;'
                  ' BrowserSessionId=5fbf4be65c6f1; RGPPortalSessionID=9crc499vdovmkbi7pk1dbpald7; '
                  'RGPSessionGUID=3b7bcabfdc8ca0eba91fe3f724248402e5e1ca396e4652b7756912a7de7cbde18c6cf2d2d0288f2e67'
                  '999a7b5589145a'
    }
    _payload = '''PreventChromeAutocomplete=&random=5fcd305c03e83&iframeid=&mode=p&fctrl_1=offering_guid&offering_guid=2923df3b2bfd4c3bb16b14795c569270&fctrl_2=course_guid&course_guid=&fctrl_3=limited_to_course_guid_for_offering_guid_2923df3b2bfd4c3bb16b14795c569270&limited_to_course_guid_for_offering_guid_2923df3b2bfd4c3bb16b14795c569270=&fctrl_4=show_date&show_date={}&ftagname_0_pcount-pid-1-316074=pcount&ftagval_0_pcount-pid-1-316074=1&ftagname_1_pcount-pid-1-316074=pid&ftagval_1_pcount-pid-1-316074=316074&fctrl_5=pcount-pid-1-316074&pcount-pid-1-316074=0&ftagname_0_pcount-pid-1-6420306=pcount&ftagval_0_pcount-pid-1-6420306=1&ftagname_1_pcount-pid-1-6420306=pid&ftagval_1_pcount-pid-1-6420306=6420306&fctrl_6=pcount-pid-1-6420306&pcount-pid-1-6420306=0&ftagname_0_pcount-pid-1-6304903=pcount&ftagval_0_pcount-pid-1-6304903=1&ftagname_1_pcount-pid-1-6304903=pid&ftagval_1_pcount-pid-1-6304903=6304903&fctrl_7=pcount-pid-1-6304903&pcount-pid-1-6304903=0&ftagname_0_pcount-pid-1-6304904=pcount&ftagval_0_pcount-pid-1-6304904=1&ftagname_1_pcount-pid-1-6304904=pid&ftagval_1_pcount-pid-1-6304904=6304904&fctrl_8=pcount-pid-1-6304904&pcount-pid-1-6304904=0&ftagname_0_pcount-pid-1-6570973=pcount&ftagval_0_pcount-pid-1-6570973=1&ftagname_1_pcount-pid-1-6570973=pid&ftagval_1_pcount-pid-1-6570973=6570973&fctrl_9=pcount-pid-1-6570973&pcount-pid-1-6570973=0&ftagname_0_pcount-pid-1-6570974=pcount&ftagval_0_pcount-pid-1-6570974=1&ftagname_1_pcount-pid-1-6570974=pid&ftagval_1_pcount-pid-1-6570974=6570974&fctrl_10=pcount-pid-1-6570974&pcount-pid-1-6570974=0'''
