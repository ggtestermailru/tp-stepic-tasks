import stepic_pytest.fixtures
import urllib
import re
import random
import os

home = '/home/box'

def test_connection(s):
    try:
        resp = urllib.urlopen("http://" + s.ip + "/")
        assert resp is not None, "Failed to connect to server"
        assert re.search(r'\bnginx\b', resp.info()['Server']), "Invalid Server header in http response"
    except Exception as e:
        assert False, str(e)


def test_tree(s):
    dirs = (
        'web',
        'web/public',
        'web/public/css',
        'web/public/js',
        'web/public/img',
        'web/uploads',
    )

    checks = {
        '-d': 'does not exists',
        '-r': 'has no read perms',
        '-w': 'has no write perms',
        '-x': 'has no search perms',
    }

    try:
        for d in dirs:
            for c, p in checks.items():
                cmd = 'test {0} {1}/{2}'.format(c, home, d)
                expl = '{0}/{1} directory {2}'.format(home, d, p)
                assert s.run(cmd).succeeded, expl
    except Exception as e:
        assert False, str(e)

def test_get(s):
    try:
        data = str(random.random())
        cmd = 'echo -n {0} > {1}/web/public/test.html'.format(data, home)
        assert s.run(cmd).succeeded, "Failed to create {0}/web/public/test.html".format(home)
        url = "http://" + s.ip + "/test.html"
        resp = urllib.urlopen(url)
        assert resp.getcode() == 200, "Not-200 server response for " + url
        assert resp.read() == data, "Server returned unexpected content instead of public/test.html"
    except Exception as e:
        assert False, str(e)

def test_get_noext(s):
    try:
        url = "http://" + s.ip + "/some/never/existing/url"
        resp = urllib.urlopen(url)
        assert resp.getcode() == 404, "Server did not return 404 for " + url
    except Exception as e:
        assert False, str(e)

def test_get_upload(s):
    try:
        data = str(random.random())
        cmd = 'echo -n {0} > {1}/web/uploads/test.html'.format(data, home)
        suc = s.run(cmd)
        assert suc.succeeded, "{0}/web/uploads/test.html created".format(home)
        url = "http://" + s.ip + "/uploads/test.html"
        resp = urllib.urlopen(url)
        assert resp.getcode() == 200, "Server did not return 200 for " + url
        assert resp.read() == data, "Server returned unexpected content instead of uploads/test.html"
    except Exception as e:
        raise
        assert False, str(e)


