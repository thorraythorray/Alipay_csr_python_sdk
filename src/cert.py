from OpenSSL import crypto

class x509CertObject:

    _cert = ""
    cert_file = ""
    force = False

    def _read_cert_content(self):
        with open(self.cert_file, "r") as f:
            file_buffer = f.read()
        return file_buffer
    
    def get_cert(self):
        if not self._cert or self.force is True:
            file_buffer = self._read_cert_content()
            self._cert = crypto.load_certificate(crypto.FILETYPE_PEM, file_buffer)
        return self._cert

    @property
    def cert_obj(self):
        return self.get_cert()

    @property
    def cert_to_to_cryptography(self):
        return self.cert_obj.to_cryptography()

    @property
    def issuer(self):
        return self.cert_obj.get_issuer()
    
    @property
    def serial_num(self):
        return self.cert_obj.get_serial_number()

    @property
    def signature_algorithm_oid(self):
        return self.cert_to_to_cryptography.signature_algorithm_oid._dotted_string