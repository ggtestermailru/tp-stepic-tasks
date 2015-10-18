import stepic_pytest.fixtures
import urllib
import re
import random
import os

home = '/home/box'

def check(res):
    if res.succeeded:
        msgs = re.findall('^(?!ERROR|FAIL)^\w+:\s*(.*)\s*$', res, flags=re.M)
        if len(msgs) > 0:
            assert False, "\n".join(msgs)
    else:
        raise Exception(res)

def test_models(s):
    res = s.run('python2.7 test_l11_server.py TestModels 2>&1')
    check(res)

def test_profile(s):
    res = s.run('python2.7 test_l11_server.py TestProfile 2>&1')
    check(res)

def test_question(s):
    res = s.run('python2.7 test_l11_server.py TestQuestion 2>&1')
    check(res)

def test_answer(s):
    res = s.run('python2.7 test_l11_server.py TestAnswer 2>&1')
    check(res)
