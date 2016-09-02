__author__ = "Matthew Tuusberg"


class ApkDownloader(object):
    def __init__(self, api, output_dir):
        self.api = api
        self.output_dir = output_dir

    def download(self, bundle_id, should_raise=True):
        """
        Downloads apk from play store. Returns absolute path to apk on success, None otherwise.
        :param bundle_id: application package name
        :param should_raise: indicates whether any unhandled exceptions should be raised
        :returns downloaded apk filename, None otherwise
        """
        try:
            apk_filename = self.api.download(bundle_id, self.output_dir)
            return apk_filename
        except Exception:
            if not should_raise:
                return None

            raise
