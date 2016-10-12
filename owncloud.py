# -*- coding:utf-8 -*-

import click
import requests


class Utilies(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def auth_get(self, url):
        r = requests.get(url, auth=(self.username, self.password))
        if r.status_code == 200:
            return r.json()['ocs']
        else:
            r.raise_for_status()

    def auth_post(self, url, param):
        r = requests.post(url, param, auth=(self.username, self.password))
        if r.status_code == 200:
            return r.json()['ocs']
        else:
            r.raise_for_status()

    def auth_put(self, url, param):
        r = requests.put(url, param, auth=(self.username, self.password))
        if r.status_code == 200:
            return r.json()['ocs']
        else:
            r.raise_for_status()

    def auth_delete(self, url):
        r = requests.delete(url, auth=(self.username, self.password))
        if r.status_code == 200:
            return r.json()['ocs']
        else:
            r.raise_for_status()

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

    def __init__(self, url, username, password):
        self.base_url = '{}/ocs/v1.php/cloud'.format(url)
        self.username = username
        self.password = password
        self.utilies = Utilies(username, password)

    # users

    def add_user(self):
        url = '{}/users?format=json'.format(self.base_url)
        userid = raw_input('userid: ')
        password = raw_input('password: ')
        param = {
            'userid': userid,
            'password': password
        }
        data = self.utilies.auth_post(url, param)
        if self.utilies.check_status(data):
            print "create user ok"
        else:
            message = self.utilies.get_status_message(data)
            print 'create user error!: {}'.format(message)

    def get_users(self):
        url = '{}/users?format=json'.format(self.base_url)
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

    def _edit_user(self, userid, key, value):
        url = '{}/users/{}?format=json'.format(self.base_url, userid)
        param = {
            key: value
        }
        data = self.utilies.auth_put
        if self.utilies.check_status(data):
            print 'edit user {} ok'.format(key)
        else:
            message = self.utilies.get_status_message(data)
            print 'edit user {} error!: {}'.format(key, message)

    def edit_user_email(self, userid, value):
        return self._edit_user(userid, 'email', value)

    def edit_user_quota(self, userid, value):
        return self._edit_user(userid, 'quota', value)

    def edit_user_display(self, userid, value):
        return self._edit_user(userid, 'display', value)

    def edit_user_password(self, userid, value):
        return self._edit_user(userid, 'password', value)

    def delete_user(self, userid):
        url = '{}/users/{}?format=json'.format(self.base_url, userid)
        pass

    def get_user_groups(self, userid):
        url = '{}/users/{}/groups?format=json'.format(self.base_url, userid)
        pass

    def add_user_to_group(self, userid, groupid, create_group=False):
        url = '{}/users/{}/groups?format=json'.format(self.base_url, userid)
        param = {
            'groupid': groupid
        }
        data = self.utilies.auth_post(url, param)
        if self.utilies.check_status(data):
            print "add user to group ok"
        else:
            if self.utilies.get_status_code(data) == 102 and create_group:
                self.create_group(groupid)
                return self.add_user_to_group(self, userid, groupid)
            else:
                message = self.utilies.get_status_message(data)
                print 'add user to group error!: {}'.format(message)

    def remove_user_from_group(self, userid, groupid):
        url = '{}/users/{}/groups?format=json'.format(self.base_url, userid)
        param = {
            'groupid': groupid
        }
        pass

    def create_subadmin(self, userid, groupid):
        url = '{}/users/{}/subadmins?format=json'.format(self.base_url, userid)
        param = {
            'groupid': groupid
        }
        pass

    def remove_subadmin(self, userid, groupid):
        url = '{}/users/{}/subadmins?format=json'.format(self.base_url, userid)
        param = {
            'groupid': groupid
        }
        pass

    def get_subadmin_groups(self, userid):
        url = '{}/users/{}/subadmins?format=json'.format(self.base_url, userid)
        pass

    # groups

    def create_group(self, groupid):
        url = '{}/groups?format=json'.format(self.base_url)
        param = {
            'groupid': groupid
        }
        data = self.utilies.auth_post(url, param)
        if self.utilies.check_status(data):
            print "create group ok"
        else:
            message = self.utilies.get_status_message(data)
            print 'create group error!: {}'.format(message)


def cli():
    url = raw_input('server address: ')
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url
    username = raw_input('admin username: ')
    password = raw_input('admin password: ')
    manager = OwncloudManager(url, username, password)
    run_command(manager, 'get_users')


def run_command(manager, command_name, *args):
    func = getattr(manager, command_name, None)
    if func is None:
        print 'command not found'
    else:
        func(*args)


if __name__ == '__main__':
    cli()
