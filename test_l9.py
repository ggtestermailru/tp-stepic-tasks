import stepic_pytest.fixtures
import urllib
import re
import random
import os

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
        resp = urllib.urlopen("http://" + s.ip + ":8080/")
        assert resp is not None, "failed to connect to port gunicorn (port 8080)"
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
            u = "http://{0}:8080{1}".format(s.ip, u)
            resp = urllib.urlopen(u)
            assert resp is not None, "failed to connect to port gunicorn (port 8080)"
            assert resp.getcode() == 200, "url {0} does not returned HTTP 200".format(u)
            body = resp.read()
            assert body == 'OK', "url {0} does not returned content 'OK'".format(u)
    except Exception as e:
        assert False, str(e)

def test_content_404(s):
    try:
        resp = urllib.urlopen("http://{0}:8080/blablabla/".format(s.ip))
        assert resp is not None, "failed to connect to port gunicorn (port 8080)"
        assert resp.getcode() == 404, "URL /blabla....bla/ was expected to return 404, but returned {0}".format(resp.getcode())
    except Exception as e:
        assert False, str(e)

def test_nginx(s):
    try:
        u = "http://{0}/".format(s.ip)
        resp = urllib.urlopen(u)
        assert resp is not None, "failed to connect to port gunicorn (port 8080)"
        assert resp.getcode() == 200, "url {0} does not returned HTTP 200".format(u)
        body = resp.read()
        assert body == 'OK', "url {0} does not returned content 'OK'".format(u)
    except Exception as e:
        assert False, str(e)


