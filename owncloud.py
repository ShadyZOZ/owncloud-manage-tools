# -*- coding:utf-8 -*-

import base64
import urllib2
from xml.etree import ElementTree

USERNAME = 'admin'
PASSWORD = 'Slim.Shady'
BASE_URL = 'http://192.168.31.99/owncloud'

class Utilies(object):

    def auth_get(self, url):
        request = urllib2.Request(url)
        base64string = base64.b64encode('%s:%s' % (USERNAME, PASSWORD))
        request.add_header("Authorization", "Basic %s" % base64string)
        response = urllib2.urlopen(request)
        return response.read()

    def read_xml(self, data):
        root = ElementTree.fromstring(data)

    def check_status(self, data):
        status_code = self.get_status(data)[1]
        if status_code == '100':
            return True
        else:
            return False

    def get_status(self, data):
        root = ElementTree.fromstring(data)
        meta_node = root.find('meta')
        status_code = meta_node.find('statuscode').text
        status = meta_node.find('status').text
        return status, status_code

class OwncloudManager(object):

    utilies = Utilies()

    def get_users(self):
        url = '%s/ocs/v1.php/cloud/users' % BASE_URL
        data = self.utilies.auth_get(url)
        if self.utilies.check_status(data):
            return data
        else:
            status, status_code = self.utilies.get_status(data)
            return 'get user error!: {} {}'.format(status, status_code)


if __name__ == '__main__':
    manager = OwncloudManager()
    print manager.get_users()