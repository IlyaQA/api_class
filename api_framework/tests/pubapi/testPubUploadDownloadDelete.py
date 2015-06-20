from pubapiutils import Calls
from pubapiutils import Config
from pubapiutils import Utils
import httplib
from unittest import TestCase


class TestClass(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.no_json = 'NoJSON'
        cls.calls = Calls()
        cls.config = Config()
        cls.utils = Utils()
        cls.utils.del_test_folder()

    def setUp(self):
        self.utils.delete_all_except(['Documents'])

    def test_upload_positive(self):
        file1 = self.utils.gen_file()
        resp = self.calls.upload(file1)
        assert resp.status_code == httplib.OK
        assert resp.json['checksum']
        assert resp.json['group_id']
        checksum = resp.json['checksum']
        group_id = resp.json['group_id']
        entry_id = resp.json['entry_id']
        assert resp.json['entry_id']
        resp = self.calls.upload(file1)
        assert resp.status_code == httplib.OK
        assert resp.json['checksum'] == checksum
        assert resp.json['group_id'] == group_id
        assert resp.json['entry_id'] != entry_id
        status_code, file2 = self.calls.download(file_id=group_id)
        assert status_code == httplib.OK
        assert self.utils.compare(file1, file2)

    def test_upload_file_folder_already_exist_with_same_name(self):
        folder1 = self.utils.random_name()
        folder1_path = self.utils.form_standard_path(folder1)
        file1 = self.utils.gen_file(file_name=folder1)
        self.calls.create_folder(folder1)
        resp = self.calls.upload(file1)
        assert resp.status_code == httplib.FORBIDDEN
        assert resp.json['message'] == 'A folder with the same name already exists: %s' % folder1_path