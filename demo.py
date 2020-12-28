from api.request import AlipayCertApiRequest

class TestAlipayCertRequest(AlipayCertApiRequest):
    # 获取临时授权码
    method = "alipay.user.info.auth"
    req_params = {
        "scopes": '["auth_base"]', 
        "state": "init"
    }

if __name__ == "__main__":
    flag, res = TestAlipayCertRequest.req_execute()
    print(res.content)