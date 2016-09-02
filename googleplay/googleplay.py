__author__ = 'Matthew Tuusberg'

from functools import wraps
from itertools import cycle
from os import path

import config
from googleplay_api.googleplay import GooglePlayAPI as BaseApi
from googleplay_api.googleplay import LoginError, RequestError, DownloadingError


def apicall(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        obj = args[0]  # self
        obj.num_requests_made += 1
        return f(*args, **kwargs)
    return wrapper


class DeviceIdHandler(object):
    def __init__(self, device_ids):
        self.device_ids = cycle(device_ids)

    @property
    def device_id(self):
        return self.device_ids.next()


class GooglePlayApi(object):
    """
    Wrapper for unofficial googleplay-api
    Handles device_id changes over the time and reduces the complexity of api calls
    """

    num_requests_made = 0  # requests counter (class attribute)

    def __init__(self, device_ids=None):
        if device_ids is None:
            device_ids = config.DEVICE_IDS

        self.id_handler = DeviceIdHandler(device_ids)
        self._api = None

    @property
    def api(self):
        """
        returns googleplay-api instance
        """
        # we should login with different credentials after every 200 requests made to prevent blocking
        should_recreate = self.__class__.num_requests_made > 200 or self._api is None

        if should_recreate:
            self._api = BaseApi(self.id_handler.device_id)
            self._api.login()
            self.__class__.num_requests_made = 0

        return self._api

    def to_dict(self, protobuf_obj):
        return self.api.toDict(protobuf_obj)

    @apicall
    def details(self, bundle_id):
        if not bundle_id or not isinstance(bundle_id, basestring):
            raise ValueError

        return self.api.details(bundle_id)

    @apicall
    def bulk_details(self, bundle_ids):
        return self.api.bulkDetails(bundle_ids)

    @apicall
    def list(self, category, subcategory, limit=None, offset=None):
        return self.api.list(category, subcategory, limit, offset)

    @apicall
    def browse(self, category, subcategory):
        return self.api.browse(category, subcategory)

    @apicall
    def search(self, query, limit=None, offset=None):
        return self.api.search(query, limit, offset)

    @apicall
    def download(self, bundle_id, out_dir):
        """
        Downloads apk from play store. Returns absolute path to apk on success, None otherwise.
        """
        filename = path.join(out_dir, bundle_id + '.apk')
        app_details = self.details(bundle_id)

        if not app_details:
            return None

        doc = app_details.docV2

        try:
            version = doc.details.appDetails.versionCode
            offer_type = doc.offer[0].offerType

            chunks = self.api.download(bundle_id, version, offer_type)

            with open(filename, "wb") as f:
                for chunk in chunks:
                    if chunk:
                        f.write(chunk)

            return path.abspath(filename)
        except Exception:
            raise


if __name__ == '__main__':
    l = [GooglePlayApi() for i in range(3)]
    for api in l:
        print api.search('something')

    print GooglePlayApi.num_requests_made
