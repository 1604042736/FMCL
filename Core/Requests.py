import time

import requests

requests.packages.urllib3.disable_warnings()


class Requests:
    __cache = {}
    HEADERS = {
        "user-agent": "FMCL"
    }

    @staticmethod
    def get(url, try_time=0, sleep_time=1, cache=True, **kwargs):
        if cache:
            if url in Requests.__cache:
                return Requests.__cache[url]
        if "headers" not in kwargs:
            kwargs["headers"] = Requests.HEADERS

        cur_try_time = 0
        while cur_try_time <= try_time or try_time == -1:
            try:
                r = requests.get(url, **kwargs)
                Requests.__cache[url] = r
                return r
            except:
                cur_try_time += 1
                time.sleep(sleep_time)

    @staticmethod
    def post(*args, **kwargs):
        if "headers" not in kwargs:
            kwargs["headers"] = Requests.HEADERS
        return requests.post(*args, **kwargs)
