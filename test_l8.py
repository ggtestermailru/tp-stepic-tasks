import stepic_pytest.fixtures
import urllib
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import re
import random
import os

home = '/home/box'

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

def test_file_compile(s):
    try:
        cmd = 'test -r {0}/web/hello.py'.format(home)
        assert s.run(cmd).succeeded, "{0}/web/hello.py does not exists".format(home)
        cmd = 'python -m py_compile {0}/web/hello.py'.format(home)
        assert s.run(cmd).succeeded, "{0}/web/hello.py - invalid syntax".format(home)
    except Exception as e:
        assert False, str(e)

def test_connection(s):
    try:
        resp = urllib2.urlopen("http://" + s.ip + ":8080/")
        assert resp is not None, "failed to connect to port gunicorn (port 8080)"
        assert re.search(r'\bgunicorn\b', resp.info()['Server']), "Invalid Server header received from gunicorn"
    except Exception as e:
        assert False, str(e)

def test_content_gunicorn(s):
    try:
        resp = urllib2.urlopen("http://" + s.ip + ":8080/?x=1&x=2&y=3&y=")
        assert resp is not None, "failed to connect to port gunicorn (port 8080)"
        assert re.search(r'^text/plain(;|$)', resp.info()['Content-Type']), "Invalid Content-Type header (text/plain expected) received from gunicorn"
        found = set([l.strip() for l in resp.readlines() ])
        for test in ('x=1', 'x=2', 'y=3', 'y='):
            assert test in found, test + ' not found in gunicorn response body'
    except Exception as e:
        assert False, str(e)

def test_content_nginx(s):
    try:
        resp = urllib2.urlopen("http://" + s.ip + "/hello/?x=1&x=2&y=3&y=")
        assert resp is not None, "failed to connect to port nginx (port 80)"
        assert re.search(r'\bnginx\b', resp.info()['Server']), "Invalid Server header received from nginx"
        assert re.search(r'^text/plain(;|$)', resp.info()['Content-Type']), "Invalid Content-Type header (text/plain expected) received from nginx"
        found = set([l.strip() for l in resp.readlines() ])
        for test in ('x=1', 'x=2', 'y=3', 'y='):
            assert test in found, test + ' not found in nginx response body'
    except Exception as e:
        assert False, str(e)


