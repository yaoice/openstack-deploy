#!/usr/bin/python

import base64
import hashlib
import json
import os
import sys
import zlib


def json_exit(msg=None, failed=False, changed=False):
    if type(msg) is not dict:
        msg = {'msg': str(msg)}
    msg.update({'failed': failed, 'changed': changed})
    print(json.dumps(msg))
    sys.exit()


def read_file(filename):
    filename_path = os.path.join('/etc/ceph', filename)

    if not os.path.exists(filename_path):
        json_exit("file not found: {}".format(filename_path), failed=True)
    if not os.access(filename_path, os.R_OK):
        json_exit("file not readable: {}".format(filename_path), failed=True)

    with open(filename_path, 'rb') as f:
        raw_data = f.read()

    return {'content': base64.b64encode(zlib.compress(raw_data)),
            'sha1': hashlib.sha1(raw_data).hexdigest(),
            'filename': filename}


def main():
    admin_keyring = 'ceph.client.admin.keyring'
    mon_keyring = 'ceph.client.mon.keyring'
    rgw_keyring = 'ceph.client.radosgw.keyring'
    monmap = 'ceph.monmap'

    files = [admin_keyring, mon_keyring, rgw_keyring, monmap]
    json_exit({filename: read_file(filename) for filename in files})


if __name__ == '__main__':
    main()
