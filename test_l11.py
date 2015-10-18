import stepic_pytest.fixtures
import urllib
import re
import random
import os

home = '/home/box'

def proxy(s, cmd):
    cmd = 'PYTHONPATH=/home/box/web/ask/ python2.7 ' + cmd + ' 2>&1'
    res = s.run(cmd)
    if res.succeeded:
        msgs = re.findall('^(?!ERROR|FAIL)^\w+:\s*(.*)\s*$', res, flags=re.M)
        if len(msgs) > 0:
            assert False, "\n".join(msgs)
    else:
        raise Exception(res)

def test_models(s):
    proxy('test_l11_server.py TestModels')

def test_profile(s):
    proxy('test_l11_server.py TestProfile')

def test_question(s):
    proxy('test_l11_server.py TestQuestion')

def test_answer(s):
    proxy('test_l11_server.py TestAnswer')
