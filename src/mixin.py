from OpenSSL import crypto
from .cert import x509CertObject
from .encrypt import EncryptObject
from conf.config import cfg

class EncryptMixin(EncryptObject):
    pass

class x509CertMixin(x509CertObject):
    pass

class AlipayAppCertMixin(EncryptMixin, x509CertMixin):
    '''
        Alipay Application Certcificate Sn
    '''
    cert_file = cfg.app_cert_sn_path

    def get_app_cert_sn(self):
        institution = "CN=" + self.issuer.CN + "," + "OU=" + self.issuer.OU + "," + "O=" + self.issuer.O + "," + "C=" + self.issuer.C
        md5_str = institution + str(self.serial_num)
        return self.md5_encrypt(md5_str)

class AlipayRootCertMixin(EncryptMixin, x509CertMixin):
    '''
        Alipay Roor Certcificate Sn
    '''
    cert_file = cfg.alipay_root_cert_sn_path

    def get_alipay_root_cert_sn(self):
        file_buffer = self._read_cert_content()
        all_root_sn = ""
        for buf in file_buffer:
            signature_algorithm_oid = self.signature_algorithm_oid
            if signature_algorithm_oid == "1.2.840.113549.1.1":
                institution = "CN=" + self.issuer.CN + "," + "O=" + self.issuer.O + "," + "C=" + self.issuer.C
                md5_str = institution + str(self.serial_num)

                _md5_sn = self.md5_encrypt(md5_str)
                if all_root_sn:
                    all_root_sn += "_" + _md5_sn
                else:
                    all_root_sn = _md5_sn
        return all_root_sn

class AlipayCertInfoMixin(AlipayAppCertMixin, AlipayRootCertMixin):
    pass

