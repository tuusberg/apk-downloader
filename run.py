__author__ = "Matthew Tuusberg"

import os
from argparse import ArgumentParser

import requests
requests.packages.urllib3.disable_warnings()  # we need to suppress urllib3 InsecureRequestWarning/InsecurePlatformWarning

from googleplay import GooglePlayApi
from downloader import ApkDownloader


def main():
    parser = ArgumentParser()
    parser.add_argument('-bundles', '-b', nargs='*', required=True, help='list of bundle ids')
    parser.add_argument('-outdir', '-o', help='output directory, default is cli directory')

    args = parser.parse_args()

    if args.outdir:
        outdir = args.outdir
        if not os.path.exists(outdir):
            raise RuntimeError('Directory {} does not exist'.format(outdir))
    else:
        outdir = os.path.dirname(__file__)

    downloader = ApkDownloader(GooglePlayApi(), outdir)

    if args.bundles:
        for bundle_id in args.bundles:
            print 'Downloading %s ...' % bundle_id
            downloader.download(bundle_id)

if __name__ == '__main__':
    main()
