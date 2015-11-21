import stepic_pytest.fixtures
# test_l7.py
import urllib
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import random
import os
import re

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

def test_project_structure(s):
    try:
        checks = [
            ('public', '-d', 'does not exists or not directory'),
            ('public/img', '-d', 'does not exists or not directory'),
            ('public/css', '-d', 'does not exists or not directory'),
            ('public/js', '-d', 'does not exists or not directory'),
            ('uploads', '-d', 'does not exists or not directory'),
            ('etc', '-d', 'does not exists or not directory'),
        ]
        for c in checks:
            cmd = 'test {0} {1}/web/{2}'.format(c[1], home, c[0])
            assert s.run(cmd).succeeded, "{0}/web/{1} {2}".format(home, c[0], c[2])
    except Exception as e:
        assert False, str(e)

def test_404(s):
    try:
        url = "http://{0}/blabla/".format(s.ip)
        resp = urllib2.urlopen(url)
        assert resp.getcode() == 404, url + " didn't returned 404"
    except Exception as e:
        assert False, str(e)

def test_public(s):
    try:
        text = "alert(1)"
        file = "{0}/web/public/js/test.js".format(home)
        cmd = "echo -n '{0}' > {1}".format(text, file)
        assert s.run(cmd).succeeded, "Failed to create " + file
        url = "http://{0}/js/test.js".format(s.ip)
        resp = urllib2.urlopen(url)
        assert resp.getcode() == 200, url + " didn't returned 200"
        assert resp.read() == text, "{0} content does not match {1} content".format(url, file)
    except Exception as e:
        assert False, str(e)

def test_uploads(s):
    try:
        text = "alert(2)"
        file = "{0}/web/uploads/test.js".format(home)
        cmd = "echo -n '{0}' > {1}".format(text, file)
        assert s.run(cmd).succeeded, "Failed to create " + file
        url = "http://{0}/uploads/test.js".format(s.ip)
        resp = urllib2.urlopen(url)
        assert resp.getcode() == 200, url + " didn't returned 200"
        assert resp.read() == text, "{0} content does not match {1} content".format(url, file)
    except Exception as e:
        assert False, str(e)

