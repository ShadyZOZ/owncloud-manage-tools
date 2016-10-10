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

    def auth_put(self):
        pass

    def auth_delete(self):
        pass

    def check_status(self, data):
        if data['meta']['statuscode'] == 100:
            return True
        else:
            return False

    def get_status_code(self, data):
        return int(data['meta']['code'])

    def get_status_message(self, data):
        return data['meta']['message']


class OwncloudManager(object):

    base_url = ''
    username = ''
    password = ''

    def __init__(self):
        url = raw_input('server address: ')
        if not url.startswith('http://') and not url.startswith('https://'):
            base_url = 'http://' + url
        username = raw_input('admin username: ')
        password = raw_input('admin password: ')
        self.base_url = '{}/ocs/v1.php/cloud'.format(base_url)
        self.username = username
        self.password = password
        self.utilies = Utilies(username, password)

    # users

    def add_user(self):
        url = '/users?format=json'.format(self.base_url)
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
            message = self.utilies.get_status_message(data)
            print 'create user error!: {}'.format(message)

    def get_users(self):
        url = '/users?format=json'.format(self.base_url)
        data = self.utilies.auth_get(url)
        if self.utilies.check_status(data):
            users = data['data']['users']
            print '{} users registered:'.format(len(users))
            for user in users:
                print user
        else:
            message = self.utilies.get_status_message(data)
            print 'get user error!: {}'.format(message)

    def get_user(self, userid):
        url = '{}/users/{}?format=json'.format(self.base_url, userid)
        data = self.utilies.auth_get(url)
        if self.utilies.check_status(data):
            print 'user: {}'.format(userid)
            print 'email: {}'.format(data['email'])
            print 'quota: {}'.format(data['quota'])
            print 'enabled: {}'.format(data['enabled'])
        else:
            message = self.utilies.get_status_message(data)
            print 'get user error!: {}'.format(message)

    def _edit_user(self, userid, key, data):
        url = '{}/users/{}?format=json'.format(self.base_url, userid)
        para = {
            key: data
        }
        print 'edit user {}'.format(key)

    def edit_user_email(self, userid, data):
        return self._edit_user(userid, 'email', data)

    def edit_user_quota(self, userid, data):
        return self._edit_user(userid, 'quota', data)

    def edit_user_display(self, userid, data):
        return self._edit_user(userid, 'display', data)

    def edit_user_password(self, userid, data):
        return self._edit_user(userid, 'password', data)

    def delete_user(self, userid):
        url = '{}/users/{}?format=json'.format(self.base_url, userid)
        pass

    def get_user_groups(self, userid):
        url = '{}/users/{}/groups?format=json'.format(self.base_url, userid)
        pass

    def add_user_to_group(self, userid, groupid, create_group=False):
        url = '{}/users/{}/groups?format=json'.format(self.base_url, userid)
        para = {
            'groupid': groupid
        }
        data = self.utilies.auth_post(url, para)
        if self.utilies.check_status(data):
            print "add user to group ok"
        else:
            if self.utilies.get_status_code(data) == 102 and create_group:
                self.create_group(groupid)
                return self.add_user_to_group(self, userid, groupid)
            else:
                message = self.utilies.get_status_message(data)
                print 'add user to group error!: {}'.format(message)

    def remove_user_to_group(self, userid, groupid):
        url = '{}/users/{}/groups?format=json'.format(self.base_url, userid)
        para = {
            'groupid': groupid
        }
        pass

    def create_subadmin(self, userid, groupid):
        url = '{}/users/{}/subadmins?format=json'.format(self.base_url, userid)
        para = {
            'groupid': groupid
        }
        pass

    def create_group(self, groupid):
        url = '{}/groups?format=json'.format(self.base_url)
        para = {
            'groupid': groupid
        }
        data = self.utilies.auth_post(url, para)
        if self.utilies.check_status(data):
            print "create group ok"
        else:
            message = self.utilies.get_status_message(data)
            print 'create group error!: {}'.format(message)

if __name__ == '__main__':
    manager = OwncloudManager()
    manager.create_group()
