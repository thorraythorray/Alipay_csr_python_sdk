import rsa
import base64
import hashlib

class EncryptObject:
    def _fill_encrypt_key_format(self, key, head, tail):
        if key.find(head) < 0:
            key = head + key
        if key.find(tail) < 0:
            key = key + tail
        return key

    def read_private_key(self, private_key_file_path):
        with open(private_key_file_path, "r") as f:
            private_key_buf = f.read()
        private_key = self._fill_encrypt_key_format(private_key_buf, "-----BEGIN RSA PRIVATE KEY-----\n", "\n-----END RSA PRIVATE KEY-----")
        return private_key
    
    @classmethod
    def rsa2_sign(cls, message, private_key_file_path):
        private_key = cls().read_private_key(private_key_file_path)
        key = rsa.PrivateKey.load_pkcs1(private_key, format='PEM')
        signature = rsa.sign(message.encode("UTF-8"), key, 'SHA-256')
        sign = base64.b64encode(signature)    
        return sign

    @staticmethod
    def md5_encrypt(message):
        return hashlib.md5(message.encode(encoding='UTF-8')).hexdigest()