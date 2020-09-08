import re
import sys
import time
import random
from functools import wraps
from typing import Union
from urllib.parse import quote, urlencode, urlparse
import requests


class Tse:
    def __init__(self):
        self.author = 'Ulion.Tse'

    @staticmethod
    def time_stat(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            t1 = time.time()
            r = func(*args, **kwargs)
            t2 = time.time()
            return r
        return wrapper

    @staticmethod
    def if_none(v1, v2):
        return v1 if v1 else v2

    @staticmethod
    def get_headers(host_url, if_use_api=False,
                    if_use_referer=True, if_ajax=True):
        url_path = urlparse(host_url).path
        host_headers = {
            'Referer' if if_use_referer else 'Host': host_url,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/55.0.2883.87 Safari/537.36"}
        api_headers = {
            'Origin': host_url.split(url_path)[0] if url_path else host_url,
            'Referer': host_url,
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/55.0.2883.87 Safari/537.36"}
        if not if_ajax:
            api_headers.pop('X-Requested-With')
            api_headers.update({'Content-Type': 'text/plain'})
        return host_headers if not if_use_api else api_headers

    @staticmethod
    def check_language(from_language, to_language, language_map,
                       output_zh=None, output_auto='auto'):
        from_language = output_auto if from_language in (
            'auto', 'auto-detect') else from_language
        from_language = output_zh if output_zh and from_language in (
            'zh', 'zh-CN', 'zh-CHS', 'zh-Hans') else from_language
        to_language = output_zh if output_zh and to_language in (
            'zh', 'zh-CN', 'zh-CHS', 'zh-Hans') else to_language

        if from_language != output_auto and from_language not in language_map:
            raise TranslatorError(
                'Unsupported from_language[{}] in {}.'.format(
                    from_language, list(
                        language_map.keys())))
        elif to_language not in language_map:
            raise TranslatorError(
                'Unsupported to_language[{}] in {}.'.format(
                    to_language, list(
                        language_map.keys())))
        elif from_language != output_auto and to_language not in language_map[from_language]:
            raise TranslatorError(
                'Unsupported translation: from [{0}] to [{1}]!'.format(
                    from_language, to_language))
        return from_language, to_language


class TranslatorSeverRegion:
    @property
    def request_server_region_info(self):
        try:
            ip_address = requests.get('http://httpbin.org/ip').json()['origin']
            try:
                data = requests.get(
                    f'http://ip-api.com/json/{ip_address}',
                    timeout=10).json()
                sys.stderr.write(
                    f'Using {data.get("country")} server backend.\n')
                return data
            except requests.exceptions.Timeout:
                data = requests.post(
                    url='http://ip.taobao.com/outGetIpInfo',
                    data={'ip': ip_address, 'accessKey': 'alibaba-inc'}
                ).json().get('data')
                data.update({'countryCode': data.get('country_id')})
                return data

        except requests.exceptions.ConnectionError:
            raise TranslatorError('Unable to connect the Internet.\n')
        except BaseException:
            raise TranslatorError('Unable to find server backend.\n')


class TranslatorError(Exception):
    pass


class Google(Tse):
    def __init__(self):
        super().__init__()
        self.host_url = None
        self.cn_host_url = 'https://translate.google.cn'
        self.en_host_url = 'https://translate.google.com'
        self.request_server_region_info = REQUEST_SERVER_REGION_INFO
        self.host_headers = None
        self.language_map = None
        self.api_url = None
        self.query_count = 0
        self.output_zh = 'zh-CN'

    def _xr(self, a, b):
        size_b = len(b)
        c = 0
        while c < size_b - 2:
            d = b[c + 2]
            d = ord(d[0]) - 87 if 'a' <= d else int(d)
            d = (a % 2**32) >> d if '+' == b[c + 1] else a << d
            a = a + d & (2**32 - 1) if '+' == b[c] else a ^ d
            c += 3
        return a

    def _ints(self, text):
        ints = []
        for v in text:
            int_v = ord(v)
            if int_v < 2**16:
                ints.append(int_v)
            else:
                # unicode, emoji
                ints.append(int((int_v - 2**16) / 2**10 + 55296))
                ints.append(int((int_v - 2**16) % 2**10 + 56320))
        return ints

    def acquire(self, text, tkk):
        ints = self._ints(text)
        size = len(ints)
        e = []
        g = 0

        while g < size:
            ll = ints[g]
            if ll < 2**7:  # 128(ascii)
                e.append(ll)
            else:
                if ll < 2**11:  # 2048
                    e.append(ll >> 6 | 192)
                else:
                    if (ll & 64512) == 55296 and g + \
                            1 < size and ints[g + 1] & 64512 == 56320:
                        g += 1
                        ll = 65536 + ((ll & 1023) << 10) + (ints[g] & 1023)
                        e.append(l >> 18 | 240)
                        e.append(l >> 12 & 63 | 128)
                    else:
                        e.append(ll >> 12 | 224)
                    e.append(ll >> 6 & 63 | 128)
                e.append(ll & 63 | 128)
            g += 1

        b = tkk if tkk != '0' else ''
        d = b.split('.')
        b = int(d[0]) if len(d) > 1 else 0

        a = b
        for value in e:
            a += value
            a = self._xr(a, '+-a^+6')
        a = self._xr(a, '+-3^+b+-f')
        a ^= int(d[1]) if len(d) > 1 else 0
        if a < 0:
            a = (a & (2**31 - 1)) + 2**31
        a %= int(1E6)
        return '{}.{}'.format(a, a ^ b)

    def get_language_map(self, host_html):
        lang_list_str = re.findall(
            r"source_code_name:\[(.*?)\],", host_html)[0]
        lang_list_str = (
            '[' + lang_list_str + ']').replace('code', '"code"').replace('name', '"name"')
        lang_list = [x['code']
                     for x in eval(lang_list_str) if x['code'] != 'auto']
        return {}.fromkeys(lang_list, lang_list)

    @Tse.time_stat
    def google_api(self, query_text: str, from_language: str = 'auto',
                   to_language: str = 'en', **kwargs) -> Union[str, list]:

        self.host_url = self.cn_host_url if kwargs.get(
            'if_use_cn_host',
            None) or self.request_server_region_info.get('countryCode') == 'CN' else self.en_host_url
        self.host_headers = self.get_headers(
            self.cn_host_url, if_use_api=False)
        is_detail_result = kwargs.get('is_detail_result', False)
        proxies = kwargs.get('proxies', None)
        use_cache = kwargs.get('use_cache', False)
        sleep_seconds = kwargs.get(
            'sleep_seconds', 0.05 + random.random() / 2 + 1e-100 * 2**self.query_count)

        with requests.Session() as ss:
            host_html = ss.get(
                self.host_url,
                headers=self.host_headers,
                proxies=proxies).text
            if self.query_count == 0 or not use_cache:
                self.language_map = self.get_language_map(host_html)
            from_language, to_language = self.check_language(
                from_language, to_language, self.language_map, output_zh=self.output_zh)

            tkk = re.findall("tkk:'(.*?)'", host_html)[0]
            tk = self.acquire(query_text, tkk)
            self.api_url = (
                self.host_url +
                '/translate_a/single?client={0}&sl={1}&tl={2}&hl=zh-CN&dt=at&dt=bd&dt=ex' +
                '&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=bh&ssel=0&tsel=0&kc=1&tk=' +
                str(tk) + '&q=' + quote(query_text)).format(
                'webapp', from_language, to_language)
            r = ss.get(
                self.api_url,
                headers=self.host_headers,
                proxies=proxies)
            r.raise_for_status()
            data = r.json()
        time.sleep(sleep_seconds)
        self.query_count += 1
        return data if is_detail_result else ''.join(
            [item[0] for item in data[0] if isinstance(item[0], str)])


REQUEST_SERVER_REGION_INFO = TranslatorSeverRegion().request_server_region_info

google_ = Google()
google = google_.google_api
