import requests

TIMEOUT = 5

class RequestApi:

    @staticmethod
    def post_request(url, data, headers=None):
        header_dict = {
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
            "Cache-Control": "no-cache",
            "Connection": "Keep-Alive",
        }
        if headers is not None:
            header_dict.update(headers)
        r = requests.post(url, headers=header_dict, data=data, timeout=TIMEOUT)
        if r.status_code == 200:
            try:
                return True, r.json()
            except:
                return True, r
        else:
            return False, r

    @staticmethod
    def get_request(url, data, headers=None):
        header_dict = {
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
            "Cache-Control": "no-cache",
            "Connection": "Keep-Alive",
        }
        if headers is not None:
            header_dict.update(headers)
        r = requests.get(url, headers=header_dict, data=data, timeout=TIMEOUT)
        if r.status_code == 200:
            try:
                return True, r.json()
            except:
                return True, r
        else:
            return False, r


