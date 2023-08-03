from hashlib import sha1
from weakref import WeakKeyDictionary

from scrapy.utils.python import to_bytes
from w3lib.url import canonicalize_url

class RequestFingerprinter:

    cache = WeakKeyDictionary()

    def fingerprint(self, request):
        if request not in self.cache:
            fp = sha1()
            fp.update(to_bytes(request.method))
            fp.update(to_bytes(canonicalize_url(request.url)))
            fp.update(request.body or b'')
            self.cache[request] = fp.digest()
        return self.cache[request]