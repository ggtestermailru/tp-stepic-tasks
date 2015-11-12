import stepic_pytest.fixtures
import urllib
import re
import random
import os
from contextlib import closing

home = '/home/box'

def proxy(s, tst):
    cmd = 'PYTHONPATH={0}/web/ask/ python2.7 {0}/{1} 2>&1'.format(home, tst)
    res = s.run(cmd)
    if res.succeeded:
        msgs = re.findall('^(?!ERROR|FAIL)^\w+:\s*(.*)\s*$', res, flags=re.M)
        if len(msgs) > 0:
            assert False, "\n".join(msgs)
    else:
        raise Exception(res)

def test_init_data(s):
    proxy(s, 'server_l14.py TestImport')

def test_ask_form(s):
    proxy(s, 'server_l14.py TestAskForm')

