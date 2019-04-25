import unittest
import os
from python.Function_FileIO import FncFileHandling


class TestFileHandling(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.abs_path = "/home/pablote/git/basketball-python/toolbox/python/files"   #absolute path
        cls.rel_path = os.path.dirname(__file__) + "/files"                         #relative working directory
        FncFileHandling.create_file(cls.abs_path + "/paulCreate.txt")

    def test_create_file(self):
        self.assertEqual("createSuccess", FncFileHandling.create_file(self.abs_path + "/paulMade.txt"))
        self.assertEqual("fileExists", FncFileHandling.create_file(self.abs_path + "/paulRead.txt"))

    def test_read_file(self):
        self.assertEqual(2, FncFileHandling.read_line(self.abs_path + "/paulRead.txt"))
        self.assertEqual(2, FncFileHandling.read_line(self.rel_path + "/paulRead.txt"))
        self.assertEqual("openFailed", FncFileHandling.read_line(self.rel_path + "/paulo.txt"))
        self.assertEqual("line1\nline2", FncFileHandling.read_string(self.rel_path + "/paulRead.txt", 0))
        self.assertEqual("line", FncFileHandling.read_string(self.rel_path + "/paulRead.txt", 4))
        self.assertEqual("openFailed", FncFileHandling.read_string(self.rel_path + "/paulo.txt", 0))

    def test_append_file(self):
        self.assertEqual(3, FncFileHandling.append_line(self.abs_path + "/paulAppend.txt", "Appended"))    #exists
        self.assertEqual(1, FncFileHandling.append_line(self.abs_path + "/paulAppender.txt", "Appended"))  #not exist

    def test_delete_file(self):
        self.assertEqual("deleteSuccess", FncFileHandling.delete_file(self.abs_path + "/paulCreate.txt"))
        self.assertEqual("fileNotFound", FncFileHandling.delete_file(self.abs_path + "/paulFish.txt"))

    @classmethod
    def tearDownClass(cls):
        FncFileHandling.remove_line(cls.abs_path + "/paulAppend.txt", "Appended")
        FncFileHandling.delete_file(cls.abs_path + "/paulAppender.txt")
        FncFileHandling.delete_file(cls.abs_path + "/paulMade.txt")
