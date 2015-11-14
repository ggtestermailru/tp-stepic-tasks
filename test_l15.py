import stepic_pytest.fixtures
import urllib
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


class NoRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        infourl = urllib.addinfourl(fp, headers, req.get_full_url())
        infourl.status = code
        infourl.code = code
        return infourl
    http_error_300 = http_error_302
    http_error_301 = http_error_302
    http_error_303 = http_error_302
    http_error_307 = http_error_302

def test_signup(s):
    try:
        urllib2.install_opener(urllib2.build_opener())
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
        urllib2.install_opener(urllib2.build_opener(NoRedirectHandler))
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
        urllib2.install_opener(urllib2.build_opener())
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
        urllib2.install_opener(urllib2.build_opener(NoRedirectHandler))
        resp = urllib2.urlopen(req)
        assert resp is not None, "failed to connect to port nginx (port 80)"
        assert str(resp.getcode()) == '302', "POST to " + url + " didn't returned 302"
        sc = resp.info().get('set-cookie', '')
        match = re.search(r'sessionid=(\w+)', sc)
        assert match is not None, "session cookie is not set on {0} page".format(url)
    except Exception as e:
        assert False, str(e)

