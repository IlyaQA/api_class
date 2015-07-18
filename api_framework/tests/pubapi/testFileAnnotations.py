import httplib
from pubapiutils import TestCaseClass


class TestClass(TestCaseClass):

    def test_upload_file_folder_already_exist_with_same_name(self):
        file1 = self.utils.gen_file()
        file1_path = self.utils.form_standard_path(file1)
        resp = self.calls.upload(file1)
        assert resp.status_code == httplib.OK
        resp = self.calls.add_file_annotation(path=file1_path, note='test')
        for i in range(100):
            print(i)
            self.calls.add_file_annotation(path=file1_path, note='test%s' % i)