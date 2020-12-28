# alipay-python-csr-sdk
alipay open api csr auth request api

支付宝开放平台的python sdk中没有支持csr模式的认证和请求，而且从官方文档中看到的价签步骤过于简单，所以按照java的方式以及网上一些博客和资料，简单构造了csr方式的python访问脚本。可以移植到工程文件中，修改路径进行填补。


安装
---

```shell
pip install openssl-python
```

定义参数
---

在conf文件中的config文件中，定义好appid以及证书的路径，脚本上会自动解析证书的需要参数。

测试
---

运行demo.py文件，打印结果。

当前只写了获取临时授权码的api，登录授权后就可以获取到访问令牌。而且对于根证书的sn获取python的方法有问题，当前因为这个值长期不会变，随意暂时写死。
