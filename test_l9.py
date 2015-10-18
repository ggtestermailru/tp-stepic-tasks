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


'''
mkdir -p /home/box/web/public
mkdir -p /home/box/web/public/js
mkdir -p /home/box/web/public/css
mkdir -p /home/box/web/public/img
mkdir -p /home/box/web/uploads/
mkdir -p /home/box/web/etc/
cat > /home/box/web/etc/nginx.conf <<EOC
server {
    listen 80 default_server;
    location / {
        proxy_pass http://127.0.0.1:8080/;
    }
    location ~ \.\w\w\w?\w?$ {
        root /home/box/web/public/;
    }
    location ^~ /uploads/ {
        alias /home/box/web/uploads/;
    }
}
EOC
sudo unlink /etc/nginx/sites-enabled/default
sudo ln -s /home/box/web/etc/nginx.conf  /etc/nginx/sites-enabled/default
sudo /usr/sbin/nginx -c /etc/nginx/nginx.conf
sudo /etc/init.d/nginx restart

(cd /home/box/web && django-admin startproject ask)
(cd /home/box/web/ask && python2.7 manage.py startapp qa)

cat > /home/box/web/ask/ask/urls.py <<EOC
from django.conf.urls import patterns, include, url
from qa.views import test
urlpatterns = patterns('',
    url(r'^$', test, name='home'),
    url(r'login/$', test, name='login'),
    url(r'signup/$', test, name='signup'),
    url(r'ask/$', test, name='ask'),
    url(r'popular/$', test, name='popular'),
    url(r'new/$', test, name='new'),
    url(r'question/(?P<id>\d+)/$', test, name='question'),
)
EOC

cat > /home/box/web/ask/qa/views.py <<EOC
from django.shortcuts import render
from django.http import HttpResponse
def test(request, *args, **kwargs):
    return HttpResponse('OK')
EOC

cat > /home/box/web/etc/django <<EOC
CONFIG = {
    'working_dir': '/home/box/web/ask',
    'args': (
        '--bind=0.0.0.0:8080',
        '--workers=3',
        '--timeout=60',
        'ask.wsgi:application',
    ),
}
EOC
sudo ln -s /home/box/web/etc/django /etc/gunicorn.d/django
sudo /etc/init.d/gunicorn restart
'''
