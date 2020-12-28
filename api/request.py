# encoding:utf-8
'''
支付宝开放平台公钥证书签名api
'''
import json
import datetime
from src.mixin import AlipayCertInfoMixin
from src.baseapi import RequestApi
from conf.config import cfg

class AlipayCertApiRequest(AlipayCertInfoMixin, RequestApi):
    app_id = cfg.app_id
    method = ""
    format = "json"
    charset = cfg.charset
    sign_type = "RSA2"
    sign = ""
    timestamp = ""
    version = "1.0"
    biz_content = ""
    return_url = ""
    if not cfg.return_url:
        return_url = cfg.return_url
    getway_url = "https://openapi.alipay.com/gateway.do"
    if not cfg.getway_url:
        self.getway_url = getway_url

    def construct_params(self):
        common_param = {
            "app_id": self.app_id,
            "method": self.method,
            "charset": self.charset,
            "sign_type": self.sign_type,
            "sign": self.sign,
            "timestamp": self.timestamp,
            "version": self.version,
            "biz_content": self.biz_content
        }
        if self.return_url:
            common_param.update({"return_url": self.return_url})

        time_now_str = datetime.datetime.now()
        time_now = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
        common_param["timestamp"] = time_now

        return common_param        

    def _joint_cert_sign_str(self, sign_params):
        if "sign" in sign_params.keys():
            del sign_params["sign"]

        app_cert_sn = self.get_app_cert_sn()
        alipay_root_cert_sn = self.get_alipay_root_cert_sn()
        # py3对根证书的序列号提取貌似有些不准确,暂时写死
        sign_params["alipay_root_cert_sn"] = "687b59193f3f462dd5336e5abf83c5d8_02941eef3187dddf3d3b83462e1dfcf6"
        sign_params["app_cert_sn"] = app_cert_sn

        sign_str = ""
        for k in sorted(sign_params):
            sign_str += str(k) + "=" + str(sign_params[k]) + "&"

        return sign_str[:-1]

    def do_cert_sign(self):
        sign_params = self.construct_params()
        sign_str = self._joint_cert_sign_str(sign_params)
        sign = self.rsa2_sign(sign_str, cfg.app_private_key_path)
        sign_params["sign"] = sign.decode(self.charset)
        
        return sign_params
    
    @classmethod
    def req_execute(cls):
        self = cls()
        signed_param = self.do_cert_sign()
        # TO DO: add pararms check
        flag, res = cls.post_request(self.getway_url, signed_param)

        return flag, res

    def get_user_info_auth(self, req_params=None):
        if req_params is None:
            req_params = {
                "scopes": '["auth_base"]', 
                "state": "init"
            }
        method_params = {
            "biz_content": json.dumps(req_params),
            "method": "alipay.user.info.auth"
        }
        signed_param = self.do_cert_sign(method_params)
        flag, res = self.post_request(signed_param)

        return flag, res

    
if __name__ == "__main__":
    flag, res = AlipayCertApiRequest().get_user_info_auth()
    