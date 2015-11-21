import stepic_pytest.fixtures
# test_l15.py
import urllib
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import re
import random
import os
from contextlib import closing

home = '/home/box'

r = str(random.randint(0, 100000))
username = 'user_test_' + r
email = 'user_' + r + '@gmail.com'
password = 'test' + r
sessionid = None
q_id = None

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

def test_signup(s):
    try:
        url = "http://" + s.ip + "/signup/"
        resp = urllib2.urlopen(url)
        assert resp is not None, "failed to connect to port nginx (port 80)"
        assert str(resp.getcode()) == '200', url + " didn't returned 200"
        sc = resp.info().get('set-cookie', '')
        match = re.search(r'csrftoken=(\w+)', sc)
        assert match is not None, "csrfttoken is not set on {0} page".format(url)
        token = match.group(1)
        body = resp.read()
        assert re.search(r'name="username"', body), "There is not input with name 'username' on " + url
        assert re.search(r'name="email"', body), "There is not input with name 'email' on " + url
        assert re.search(r'name="password"', body), "There is not input with name 'password' on " + url

        data = urllib.urlencode({'username': username, 'email': email, 'password': password, 'csrfmiddlewaretoken': token })
        headers = {'Cookie': 'csrftoken=' + token}
        req = urllib2.Request(url, data, headers)
        resp = urllib2.urlopen(req)
        assert resp is not None, "failed to connect to port nginx (port 80)"
        assert str(resp.getcode()) == '302', "POST to " + url + " didn't returned 302"
        sc = resp.info().get('set-cookie', '')
        match = re.search(r'sessionid=(\w+)', sc)
        assert match is not None, "session cookie is not set on {0} page".format(url)
    except Exception as e:
        assert False, str(e)

def test_login(s):
    try:
        url = "http://" + s.ip + "/login/"
        resp = urllib2.urlopen(url)
        assert resp is not None, "failed to connect to port nginx (port 80)"
        assert str(resp.getcode()) == '200', url + " didn't returned 200"
        sc = resp.info().get('set-cookie', '')
        match = re.search(r'csrftoken=(\w+)', sc)
        assert match is not None, "csrfttoken is not set on {0} page".format(url)
        token = match.group(1)
        body = resp.read()
        assert re.search(r'name="username"', body), "There is not input with name 'username' on " + url
        assert re.search(r'name="password"', body), "There is not input with name 'password' on " + url

        data = urllib.urlencode({'username': username, 'password': password, 'csrfmiddlewaretoken': token })
        headers = {'Cookie': 'csrftoken=' + token}
        req = urllib2.Request(url, data, headers)
        resp = urllib2.urlopen(req)
        assert resp is not None, "failed to connect to port nginx (port 80)"
        assert str(resp.getcode()) == '302', "POST to " + url + " didn't returned 302"
        sc = resp.info().get('set-cookie', '')
        match = re.search(r'sessionid=(\w+)', sc)
        assert match is not None, "session cookie is not set on {0} page".format(url)
        global sessionid
        sessionid = match.group(1)
    except Exception as e:
        assert False, str(e)

def test_ask_authorized(s):
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
        headers = {'Cookie': 'csrftoken=' + token + '; sessionid=' + sessionid}
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

def test_init_data(s):
    proxy(s, 'server_l15.py TestAuthorship {0} {1}'.format(username, q_id))

