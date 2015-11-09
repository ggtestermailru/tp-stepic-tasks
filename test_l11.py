import stepic_pytest.fixtures
import urllib
import re
import random
import os

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

def test_models(s):
    proxy(s, 'server_l11.py TestModels')

def test_user(s):
    proxy(s, 'server_l11.py TestUser')

def test_question(s):
    proxy(s, 'server_l11.py TestQuestion')

def test_question_manager(s):
    proxy(s, 'server_l11.py TestQuestionManager')

def test_answer(s):
    proxy(s, 'server_l11.py TestAnswer')
