import stepic_pytest.fixtures
import urllib
import re
import random
import os

home = '/home/box'

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
        resp = urllib.urlopen("http://" + s.ip + ":8080/")
        assert resp is not None, "failed to connect to port gunicorn (port 8080)"
        assert re.search(r'\bgunicorn\b', resp.info()['Server']), "Invalid Server header received from gunicorn"
    except Exception as e:
        assert False, str(e)

def test_content_gunicorn(s):
    try:
        resp = urllib.urlopen("http://" + s.ip + ":8080/?x=1&x=2&y=3&y=")
        assert resp is not None, "failed to connect to port gunicorn (port 8080)"
        assert re.search(r'^text/plain(;|$)', resp.info()['Content-Type']), "Invalid Content-Type header (text/plain expected) received from gunicorn"
        found = set([l.strip() for l in resp.readlines() ])
        for test in ('x=1', 'x=2', 'y=3', 'y='):
            assert test in found, test + ' not found in gunicorn response body'
    except Exception as e:
        assert False, str(e)

def test_content_nginx(s):
    try:
        resp = urllib.urlopen("http://" + s.ip + "/hello/?x=1&x=2&y=3&y=")
        assert resp is not None, "failed to connect to port nginx (port 80)"
        assert re.search(r'\bnginx\b', resp.info()['Server']), "Invalid Server header received from nginx"
        assert re.search(r'^text/plain(;|$)', resp.info()['Content-Type']), "Invalid Content-Type header (text/plain expected) received from nginx"
        found = set([l.strip() for l in resp.readlines() ])
        for test in ('x=1', 'x=2', 'y=3', 'y='):
            assert test in found, test + ' not found in nginx response body'
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
        return 404;
    }
    location /hello/ {
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
cat > /home/box/web/hello.py <<EOC
def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
        qs = environ.get('QUERY_STRING', '')
        for w in qs.split('&'):
            yield w + '\n'
EOC
cat > /home/box/web/etc/hello.py <<EOC
CONFIG = {
    'working_dir': '/home/box/web',
    'args': (
        '--bind=0.0.0.0:8080',
        '--workers=3',
        '--timeout=60',
        'hello:application',
    ),
}
EOC
sudo ln -s /home/box/web/etc/hello.py /etc/gunicorn.d/hello.py
sudo /etc/init.d/gunicorn restart
'''
