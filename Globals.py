import time

import requests


class Globals:
    TAG_NAME = "2.0"

    @staticmethod
    def request_keep_get(url, max_time=10):
        cur_time = 0
        while cur_time <= max_time:
            try:
                headers = {
                    "user-agent": "FMCL"
                }
                return requests.get(url, headers=headers, timeout=4)
            except requests.exceptions.RequestException as e:
                exception = e
                time.sleep(1)
                cur_time += 1
        raise exception
