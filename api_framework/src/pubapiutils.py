import requests
import json
from ConfigParser import SafeConfigParser
import os
from random import randint
import base64
import inspect
import random
from email.utils import formatdate
import filecmp
from requests_futures.sessions import FuturesSession as request
from concurrent.futures import ThreadPoolExecutor
from unittest import TestCase
import time


class Config:
    def __init__(self):
        self.parser = SafeConfigParser()
        if os.path.isfile('config.ini'):
            self.parser.read('config.ini')
        else:
            print('No config.ini found under root folder.')
        self.domain = self.parser.get('Server', 'url')
        self.admin_login = self.parser.get('Server', 'user')
        self.password = self.parser.get('Server', 'passwd')
        self.puser = self.parser.get('Server', 'puser')
        self.testdata = './test_files'


class TestCaseClass(TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCaseClass, self).__init__(*args, **kwargs)

    @classmethod
    def setUpClass(cls):
        cls.no_json = 'NoJSON'
        cls.config = Config()

    def setUp(self):
        self.config.testpath = '/Shared/dynamic_name_%s' % str(time.time()).replace('.', '')
        self.utils = Utils(self.config)
        self.calls = self.utils.calls

    @classmethod
    def tearDownClass(cls):
        cls.calls = Calls(cls.config)
        cls.calls.delete_all_except('Documents')


class Calls:
    def __init__(self, config):
        self.config = config
        self.no_json = 'NoJSON'

    def add_file_annotation(self, path, note=None, content_type='application/vnd.egnyte.annotations.request+json',
                            accept='application/vnd.egnyte.annotations.response+json', method=None, username=None, password=None):
        if username is None:
            username = self.config.admin_login
        if password is None:
            password = self.config.password
        if method is None:
            method = method

        domain = self.config.domain
        endpoint = '/public-api/v1/notes'
        url = domain + endpoint
        if note is None:
            note = Utils.random_name()
        headers = dict()
        data = dict()
        data['path'] = path
        data['body'] = note

        headers['Content-Type'] = content_type
        headers['Accept'] = accept
        headers['Authorization'] = 'Basic %s' % base64.b64encode('%s:%s' % (username, password))

        data = json.dumps(data)

        session = request(executor=ThreadPoolExecutor(max_workers=10))
        r = session.request(
            method=method,
            url=url,
            headers=headers,
            data=data
        )
        return r

    def create_folder(self, folder_name, path=None, domain=None, method=None, content_type=None, accept=None,
                      username=None, password=None, print_call=True, async=None):
        if domain is None:
            domain = self.config.domain
        if method is None:
            method = 'POST'
        if content_type is None:
            content_type = 'application/json'
        if accept is None:
            accept = 'application/json'
        if username is None:
            username = self.config.admin_login
        if password is None:
            password = self.config.password
        if path is None:
            path = self.config.testpath
        if async is None:
            async = False

        endpoint = '/public-api/v1/fs'
        url = '%s%s%s/%s' % (domain, endpoint, path, folder_name)
        headers = dict()
        headers['Content-Type'] = content_type
        headers['Accept'] = accept
        data = dict()
        data['action'] = 'add_folder'
        data = json.dumps(data)

        headers['Authorization'] = 'Basic %s' % base64.b64encode('%s:%s' % (username, password))


        if not async:

            r = requests.request(
                method=method,
                url=url,
                headers=headers,
                data=data
            )

            try:
                json_resp = json.loads(r.content)
            except ValueError:
                json_resp = self.no_json

            r.json = json_resp
            if print_call:
                self.nice_print_out(call_name='Create Folder', r=r, caller=inspect.stack()[1][3])

            return r

        else:
            session = request(executor=ThreadPoolExecutor(max_workers=100))
        r = session.request(
                method=method,
                url=url,
                headers=headers,
                data=data
        )
        return r

    def delete_folder(self, name, parent_path=None, domain=None, method=None, content_type=None, accept=None,
                      username=None, password=None, print_call=True, caller=None):
        if domain is None:
            domain = self.config.domain
        if method is None:
            method = 'DELETE'
        if content_type is None:
            content_type = 'application/json'
        if accept is None:
            accept = 'application/json'
        if username is None:
            username = self.config.admin_login
        if password is None:
            password = self.config.password
        if caller is None:
            caller = inspect.stack()[1][3]

        endpoint = '/public-api/v1/fs'

        if parent_path is None:
            parent_path = self.config.testpath
        url = domain + endpoint + parent_path + '/' + name

        headers = dict()
        headers['Content-Type'] = content_type
        headers['Accept'] = accept

        headers['Authorization'] = 'Basic %s' % base64.b64encode('%s:%s' % (username, password))

        r = requests.request(
            method=method,
            url=url,
            headers=headers
        )

        try:
            json_resp = json.loads(r.content)
        except ValueError:
            json_resp = self.no_json

        r.json = json_resp
        if print_call:
            self.nice_print_out(call_name='Delete Folder', r=r, caller=caller)

        return r

    def move_item(self, name, destination, parent_path=None, domain=None, method=None, content_type=None,
                  accept=None, username=None, password=None, print_call=True):

        if domain is None:
            domain = self.config.domain
        if method is None:
            method = 'POST'
        if content_type is None:
            content_type = 'application/json'
        if accept is None:
            accept = 'application/json'
        if username is None:
            username = self.config.admin_login
        if password is None:
            password = self.config.password
        if parent_path is None:
            parent_path = self.config.testpath

        endpoint = '/public-api/v1/fs'
        url = '%s%s%s/%s' % (domain, endpoint, parent_path, name)
        headers = dict()
        headers['Content-Type'] = content_type
        headers['Accept'] = accept
        data = dict()
        data['action'] = 'move'
        data['destination'] = destination + '/' + name
        data = json.dumps(data)

        headers['Authorization'] = 'Basic %s' % base64.b64encode('%s:%s' % (username, password))

        r = requests.request(
            method=method,
            url=url,
            headers=headers,
            data=data
        )

        try:
            json_resp = json.loads(r.content)
        except ValueError:
            json_resp = self.no_json

        r.json = json_resp
        if print_call:
            self.nice_print_out(call_name='Move Item', r=r, caller=inspect.stack()[1][3])

        return r

    def set_perms(self, folder_path, users, permission, domain=None, method=None, content_type=None, accept=None,
                  username=None, password=None, print_call=True):
        if domain is None:
            domain = self.config.domain
        if method is None:
            method = 'POST'
        if content_type is None:
            content_type = 'application/json'
        if accept is None:
            accept = 'application/json'
        if username is None:
            username = self.config.admin_login
        if password is None:
            password = self.config.password

        endpoint = '/public-api/v1/perms/folder'
        url = '%s%s%s' % (domain, endpoint, folder_path)
        headers = dict()
        headers['Content-Type'] = content_type
        headers['Accept'] = accept
        data = dict()
        data['users'] = []
        data['permission'] = permission
        if type(users) == list:
            for user in users:
                data['users'].append(user)
        else:
            data['users'].append(users)
        data = json.dumps(data)

        headers['Authorization'] = 'Basic %s' % base64.b64encode('%s:%s' % (username, password))

        r = requests.request(
            method=method,
            url=url,
            headers=headers,
            data=data
        )

        try:
            json_resp = json.loads(r.content)
        except ValueError:
            json_resp = self.no_json

        r.json = json_resp
        if print_call:
            self.nice_print_out(call_name='Set Permissions', r=r, caller=inspect.stack()[1][3])

        return r

    def list_perms(self, folder_path, users, domain=None, method=None, content_type=None, accept=None,
                   username=None, password=None, print_call=True):
        if domain is None:
            domain = self.config.domain
        if method is None:
            method = 'GET'
        if content_type is None:
            content_type = 'application/json'
        if accept is None:
            accept = 'application/json'
        if username is None:
            username = self.config.admin_login
        if password is None:
            password = self.config.password

        endpoint = '/public-api/v1/perms/folder'
        url = '%s%s%s' % (domain, endpoint, folder_path)
        headers = dict()
        headers['Content-Type'] = content_type
        headers['Accept'] = accept

        url += '?users=%s' % users

        headers['Authorization'] = 'Basic %s' % base64.b64encode('%s:%s' % (username, password))

        r = requests.request(
            method=method,
            url=url,
            headers=headers
        )

        try:
            json_resp = json.loads(r.content)
        except ValueError:
            json_resp = self.no_json

        r.json = json_resp
        if print_call:
            self.nice_print_out(call_name='List Permissions', r=r, caller=inspect.stack()[1][3])

        return r

    def list_folders(self, folder_path, domain=None, method=None, content_type=None, accept=None, username=None,
                     password=None, print_call=True, caller=None, allow_link_type=None, perms=None, include_perm=None,
                     list_content=None):

        if domain is None:
            domain = self.config.domain
        if method is None:
            method = 'GET'
        if content_type is None:
            content_type = 'application/json'
        if accept is None:
            accept = 'application/json'
        if username is None:
            username = self.config.admin_login
        if password is None:
            password = self.config.password
        if caller is None:
            caller = inspect.stack()[1][3]

        endpoint = '/public-api/v1/fs'
        url = '%s%s%s' % (domain, endpoint, folder_path)
        headers = dict()
        headers['Content-Type'] = content_type
        headers['Accept'] = accept

        headers['Authorization'] = 'Basic %s' % base64.b64encode('%s:%s' % (username, password))

        params = dict()
        if list_content is not None:
            params['list_content'] = list_content
        if allow_link_type is not None:
            params['allowed_link_types'] = allow_link_type
        if perms is not None:
            params['perms'] = perms
        if include_perm is not None:
            params['include_perm'] = include_perm

        r = requests.request(
            method=method,
            url=url,
            headers=headers,
            params=params
        )

        try:
            json_resp = json.loads(r.content)
        except ValueError:
            json_resp = self.no_json

        r.json = json_resp
        if print_call:
            self.nice_print_out(call_name='List Folders', r=r, caller=caller)

        return r

    def upload(self, filename, path=None, time1=None, server=None, username=None, password=None, name=None,
               content_type=None, print_call=True, method=None):
        if server is None:
            server = self.config.domain
        if name is None:
            name = os.path.basename(filename)
        if time1 is None:
            time1 = formatdate()
        if path is None:
            path = self.config.testpath
        if method is None:
            method = 'POST'
        if username is None:
            username = self.config.admin_login
        if password is None:
            password = self.config.password

        headers = dict()
        headers['Authorization'] = 'Basic %s' % base64.b64encode('%s:%s' % (username, password))
        headers['Last-Modified'] = time1

        if content_type is not None:
            headers['Content-type'] = content_type

        url = server + '/public-api/v1/fs-content' + path + '/' + name

        local_file_path = '%s/%s' % (self.config.testdata, filename)

        r = requests.request(
            url=url,
            headers=headers,
            data=open(local_file_path, 'rb'),
            method=method
        )

        try:
            json_resp = json.loads(r.content)
        except ValueError:
            if method == 'OPTIONS':
                json_resp = r.content
            else:
                json_resp = self.no_json

        r.request.body = '<FILE_DATA> at %s' % local_file_path
        r.json = json_resp
        if print_call:
            self.nice_print_out(call_name='Upload File', r=r, caller=inspect.stack()[1][3])

        return r

    def download(self, filename=None, file_id=None, entry_id=None, path=None, server=None, username=None,
                 password=None):
        if server is None:
            server = self.config.domain
        if path is None and filename is None and file_id:
            url = server + '/public-api/v1/fs-content/ids/file/' + file_id
        elif path is None and not file_id:
            url = server + '/public-api/v1/fs-content' + self.config.testpath + '/' + filename
        else:
            url = server + '/public-api/v1/fs-content' + path + '/' + filename
        if username is None:
            username = self.config.admin_login
        if password is None:
            password = self.config.password

        if entry_id is not None:
            url += '?entry_id=%s' % entry_id

        headers = dict()

        headers['Authorization'] = 'Basic %s' % base64.b64encode('%s:%s' % (username, password))

        r = requests.get(
            url=url,
            headers=headers,
            stream=True
        )

        try:
            json_resp = json.loads(r.content)
        except ValueError:

            file1 = Utils.random_name()
            with open(self.config.testdata + '/' + file1, 'wb') as f:
                for chunk in r.iter_content(1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()
            return r.status_code, file1
        r.json = json_resp
        return r

    @staticmethod
    def nice_print_out(call_name, r, caller):
        header_string = ''
        for key in r.request.headers:
            header_string += '-H "%s: %s" ' % (key, r.request.headers[key])
        print('\n*TestCase Name: %s, API Call: %s*' % (caller, call_name))
        if r.request.body:
            print('Curl is:\n curl %s "%s" -d \'%s\' -X %s' % (header_string, r.request.url, r.request.body,
                                                               r.request.method))
        else:
            print('Curl is:\n curl %s "%s" -X %s' % (header_string, r.request.url, r.request.method))
        print('\nResponse status code: %s' % r.status_code)
        if r.json != 'NoJSON':
            try:
                print('\nResponse body:\n %s' % json.dumps(r.json, indent=2))
            except TypeError:
                print('\nResponse body:\n %s' % r.json)
        else:
            print('\nNo body in the response.')

    def delete_all_except(self, l):
        resp = self.list_folders(folder_path='/Shared', caller='Cleanup')
        l1 = resp.json

        for i in range(len(l1['folders'])):
            if l1['folders'][i]['name'] in l:
                l1['folders'][i] = None

        while l1['folders'].count(None) != len(l1['folders']):
            for elem in l1['folders']:
                if elem is not None:
                    self.delete_folder(parent_path='/Shared', name=elem['name'], caller='Cleanup')
                    index = l1['folders'].index(elem)
                    del l1['folders'][index]


class Utils:
    def __init__(self, config):
        self.config = config
        self.calls = Calls(config)

    @staticmethod
    def random_name():
        return 'test_name%s' % randint(1000000, 9999999)

    @staticmethod
    def compare(file1, file2):
        return filecmp.cmp(Config().testdata + '/' + file1, Config().testdata + '/' + file2)

    def delete_all_except(self, l):
        resp = self.calls.list_folders(folder_path='/Shared', caller='Cleanup')
        l1 = resp.json

        for i in range(len(l1['folders'])):
            if l1['folders'][i]['name'] in l:
                l1['folders'][i] = None

        while l1['folders'].count(None) != len(l1['folders']):
            for elem in l1['folders']:
                if elem is not None:
                    self.calls.delete_folder(parent_path='/Shared', name=elem['name'], caller='Cleanup')
                    index = l1['folders'].index(elem)
                    del l1['folders'][index]

    def form_standard_path(self, name):
        return '%s/%s' % (self.config.testpath, name)

    def gen_file(self, file_name=None, block_size=None, num_blocks=None, text=None):
        if block_size is None:
            block_size = 200
        if num_blocks is None:
            num_blocks = 1
        if file_name is None:
            file_name = 'test_filename_' + str(random.randint(1, 10000000)) + '.txt'
        file_path = '%s/%s' % (self.config.testdata, file_name)
        if not os.path.exists(self.config.testdata):
                cmd = 'mkdir %s' % self.config.testdata
                os.system(cmd)
        if not os.path.isfile('.test_files/%s' % file_name) and text is None:
            cmd = "dd if=/dev/urandom of='%s' bs=%d count=%d 2>/dev/null" % (file_path, block_size, num_blocks)
            os.system(cmd)
        elif text is not None:
            cmd = 'echo "%s" > %s' % (text, file_path)
            os.system(cmd)
        return file_name

    def del_test_folder(self):
        cmd = 'rm -rf %s' % self.config.testdata
        os.system(cmd)