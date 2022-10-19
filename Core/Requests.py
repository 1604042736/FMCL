import time

import requests

requests.packages.urllib3.disable_warnings()


class Requests:
    @staticmethod
    def get(url, try_time=0, sleep_time=1, **kwargs):
        if "headers" not in kwargs:
            kwargs["headers"] = {
                "user-agent": "FMCL"
            }
        cur_try_time = 0
        while cur_try_time <= try_time or try_time == -1:
            try:
                return requests.get(url, **kwargs)
            except:
                cur_try_time += 1
                time.sleep(sleep_time)
