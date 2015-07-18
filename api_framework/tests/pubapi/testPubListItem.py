import httplib
from pubapiutils import TestCaseClass


class TestClass(TestCaseClass):

    def test_list_folder_links_params(self):
        folder = self.utils.random_name()
        self.calls.create_folder(folder)
        resp = self.calls.list_folders(folder_path=self.config.testpath, allow_link_type=True, perms=True,
                                       list_content=True)
        assert resp.status_code == httplib.OK
        assert resp.json == 1