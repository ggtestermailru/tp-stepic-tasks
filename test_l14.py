import stepic_pytest.fixtures
import urllib
import urllib2
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

def test_add_question(s):
    try:
        url = "http://" + s.ip + "/ask/"
        resp = urllib2.urlopen(url)
        assert resp is not None, "failed to connect to port nginx (port 80)"
        assert str(resp.getcode()) == '200', url + " didn't returned 200"
        sc = resp.info().get('set-cookie', '')
        match = re.search(r'csrftoken=(\w+)', sc)
        assert match is not None, "csrfttoken is not set on {0} page".format(url)
        token = match.group(1)
        data = urllib.urlencode({'title':'x123','text':'2bo!2b?', 'csrfmiddlewaretoken': token })
        headers = {'Cookie': 'csrftoken=' + token}
        req = urllib2.Request(url, data, headers)
        resp = urllib2.urlopen(req)
        assert resp is not None, "failed to connect to port nginx (port 80)"
        assert str(resp.getcode()) == '200', "POST to " + url + " didn't returned 200"
        url = resp.geturl()
        assert re.search(r'/question/\d+/?', url), "POST to " + url + " didn't redirected to question page"
    except Exception as e:
        assert False, str(e)
