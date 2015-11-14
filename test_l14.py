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

class DaHandler(urllib2.HTTPRedirectHandler):
    def handle(self, req, fp, code, msg, headers):
        infourl = urllib.addinfourl(fp, headers, req.get_full_url())
        infourl.status = code
        infourl.code = code
        return infourl
    http_error_300 = handle
    http_error_301 = handle
    http_error_302 = handle
    http_error_303 = handle
    http_error_307 = handle
    http_error_401 = handle
    http_error_403 = handle
    http_error_404 = handle
    http_error_500 = handle
    http_error_502 = handle
    http_error_504 = handle

urllib2.install_opener(urllib2.build_opener(DaHandler))

def test_init_data(s):
    proxy(s, 'server_l14.py TestImport')

def test_ask_form(s):
    proxy(s, 'server_l14.py TestAskForm')

def test_answer_form(s):
    proxy(s, 'server_l14.py TestAnswerForm')

q_id = None

def test_ask(s):
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
        assert str(resp.getcode()) == '302', "POST to " + url + " didn't redirected to question page"
        url = resp.info().get('location')
        match = re.search(r'/question/(\d+)/?', url)
        assert match is not None, "POST to " + url + " didn't redirected to question page"
        global q_id
        q_id = match.group(1)
    except Exception as e:
        assert False, str(e)

def test_answer(s):
    try:
        url = "http://" + s.ip + "/question/" + str(q_id) + "/"
        resp = urllib2.urlopen(url)
        assert resp is not None, "failed to connect to port nginx (port 80)"
        assert str(resp.getcode()) == '200', url + " didn't returned 200"
        sc = resp.info().get('set-cookie', '')
        match = re.search(r'csrftoken=(\w+)', sc)
        assert match is not None, "csrfttoken is not set on {0} page".format(url)
        token = match.group(1)
        data = urllib.urlencode({'text': '2b', 'question_id': q_id, 'csrfmiddlewaretoken': token })
        headers = {'Cookie': 'csrftoken=' + token}
        req = urllib2.Request(url, data, headers)
        resp = urllib2.urlopen(req)
        assert resp is not None, "failed to connect to port nginx (port 80)"
        assert str(resp.getcode()) == '200', "POST to " + url + " didn't returned 200"
        url = resp.geturl()
        assert re.search(r'/question/\d+/?', url), "POST to " + url + " didn't redirected to question page"
    except Exception as e:
        assert False, str(e)
