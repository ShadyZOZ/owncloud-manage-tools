# -*- coding:utf-8 -*-

import base64
import urllib
import urllib2
import json

class Utilies(object):


    def __init__(self, username, password):
        self.username = username
        self.password = password


    def auth_get(self, url):
        request = urllib2.Request(url)
        base64string = base64.b64encode('%s:%s' % (self.username, self.password))
        request.add_header("Authorization", "Basic %s" % base64string)
        response = urllib2.urlopen(request)
        data = response.read()
        return json.loads(data)['ocs']

    def auth_post(self, url, para_dict):
        para_data = urllib.urlencode(para_dict)
        request = urllib2.Request(url, para_data)
        base64string = base64.b64encode('%s:%s' % (self.username, self.password))
        request.add_header("Authorization", "Basic %s" % base64string)
        response = urllib2.urlopen(request)
        data = response.read()
        return json.loads(data)['ocs']

    def check_status(self, data):
        if data['meta']['statuscode'] == 100:
            return True
        else:
            return False

    def get_status(self, data):
        return data['meta']['status'], data['meta']['statuscode'], data['meta']['message']

class OwncloudManager(object):

    base_url = ''
    username = ''
    password = ''


    def __init__(self):
        base_url = raw_input('server address: ')
        if not base_url.startswith('http://') and not base_url.startswith('https://'):
            base_url = 'http://' + base_url
        username = raw_input('admin username: ')
        password = raw_input('admin password: ')
        self.base_url = base_url
        self.username = username
        self.password = password
        self.utilies = Utilies(username, password)

    def get_users(self):
        url = '{}/ocs/v1.php/cloud/users?format=json'.format(self.base_url)
        data = self.utilies.auth_get(url)
        if self.utilies.check_status(data):
            users = data['data']['users']
            print '{} users registered:'.format(len(users))
            for user in users:
                print user
        else:
            status, status_code, message = self.utilies.get_status(data)
            print 'get user error!: {}'.format(message)

    def get_user(self, userid):
        url = '{}/ocs/v1.php/cloud/users/{}?format=json'.format(self.base_url, userid)
        data = self.utilies.auth_get(url)
        if self.utilies.check_status(data):
            print data
        else:
            status, status_code, message = self.utilies.get_status(data)
            print 'get user error!: {}'.format(message)

    def created_user(self):
        url = '{}/ocs/v1.php/cloud/users?format=json'.format(self.base_url)
        userid = raw_input('userid: ')
        password = raw_input('password: ')
        para = {
            'userid': userid,
            'password': password
        }
        data = self.utilies.auth_post(url, para)
        if self.utilies.check_status(data):
            print "create user ok"
        else:
            status, status_code, message = self.utilies.get_status(data)
            print 'create user error!: {}'.format(message)

    def create_group(self):
        url = '{}/ocs/v1.php/cloud/groups?format=json'.format(self.base_url)
        groupid = raw_input('groupid: ')
        para = {
            'groupid': groupid
        }
        data = self.utilies.auth_post(url, para)
        if self.utilies.check_status(data):
            print "create group ok"
        else:
            status, status_code, message = self.utilies.get_status(data)
            print 'create group error!: {}'.format(message)

    def add_user_to_group(self):
        userid = raw_input('userid: ')
        url = '{}/ocs/v1.php/cloud/users/{}/groups?format=json'.format(self.base_url, userid)
        groupid = raw_input('groupid: ')
        para = {
            'groupid': groupid
        }
        data = self.utilies.auth_post(url, para)
        if self.utilies.check_status(data):
            print "add user to group ok"
        else:
            status, status_code, message = self.utilies.get_status(data)
            print 'add user to group error!: {}'.format(message)

if __name__ == '__main__':
    manager = OwncloudManager()
    while True:
        command = raw_input('owncloud> ').split(' ')
        if command[0] == 'reset':
            manager = OwncloudManager()
        elif command[0] == 'exit':
            print 'exit owncloud tool shell'
            return
        elif command[0] == 'get_users':
            pass
        else:
            print 'unknown command'

    manager.create_group()
