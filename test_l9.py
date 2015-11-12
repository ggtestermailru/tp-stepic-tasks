import stepic_pytest.fixtures
import urllib
import random
import os
import re

home = '/home/box'

def test_project_structure(s):
    try:
        checks = [
            ('ask', '-d', 'does not exists or not directory'),
            ('ask/qa', '-d', 'does not exists or not directory'),
            ('ask/ask', '-d', 'does not exists or not directory'),
            ('ask/manage.py', '-f', 'does not exists or not a file'),
            ('ask/ask/settings.py', '-f', 'does not exists or not a file'),
            ('ask/qa/views.py', '-f', 'does not exists or not a file'),
        ]
        for c in checks:
            cmd = 'test {0} {1}/web/{2}'.format(c[1], home, c[0])
            assert s.run(cmd).succeeded, "{0}/web/{1} {2}".format(home, c[0], c[2])
    except Exception as e:
        assert False, str(e)

def test_connection(s):
    try:
        resp = urllib.urlopen("http://" + s.ip + ":8000/")
        assert resp is not None, "failed to connect to port gunicorn (port 8000)"
    except Exception as e:
        assert False, str(e)

def test_content_gunicorn(s):
    try:
        urls = [
            '/',
            '/login/',
            '/signup/',
            '/question/321/',
            '/question/77/',
            '/ask/'
            '/popular/',
            '/new/',
        ]
        for u in urls:
            u = "http://{0}:8000{1}".format(s.ip, u)
            resp = urllib.urlopen(u)
            assert resp is not None, "failed to connect to port gunicorn (port 8000)"
            if not re.search(r'/question/', u):
                assert resp.getcode() == 200, "url {0} does not returned HTTP 200".format(u)
            body = resp.read()
            assert re.search(r'\w', body), "url {0} : body is empty {1}".format(u, body)
    except Exception as e:
        assert False, str(e)

def test_content_404(s):
    try:
        resp = urllib.urlopen("http://{0}:8000/blablabla/".format(s.ip))
        assert resp is not None, "failed to connect to port gunicorn (port 8000)"
        assert resp.getcode() == 404, "URL /blabla....bla/ was expected to return 404, but returned {0}".format(resp.getcode())
    except Exception as e:
        assert False, str(e)

def test_nginx(s):
    try:
        u = "http://{0}/".format(s.ip)
        resp = urllib.urlopen(u)
        assert resp is not None, "failed to connect to port gunicorn (port 8000)"
        assert resp.getcode() == 200, "url {0} does not returned HTTP 200 {1}".format(u, body)
        body = resp.read()
        assert re.search(r'\w', body), "url {0} : body is empty".format(u)
    except Exception as e:
        assert False, str(e)


