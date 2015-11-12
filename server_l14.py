import os
import unittest
import sys
sys.path.append('/home/box/web/ask')
os.environ['DJANGO_SETTINGS_MODULE'] = 'ask.settings'

class TestImport(unittest.TestCase):
    def test_import(self):
        import qa.forms

class TestAskForm(unittest.TestCase):
    def test_from(self):
        from qa.forms import AskForm

suite = unittest.TestLoader().loadTestsFromTestCase(globals().get(sys.argv[1]))
unittest.TextTestRunner(verbosity=0).run(suite)
