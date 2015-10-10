import stepic_pytest.fixtures
import urllib
import re
import random
import os

home = os.environ.get('HOME')
#home = '/home/box'

def test_connection(s):
    try:
        resp = urllib.urlopen("http://" + s.ip + "/")
        assert resp is not None, "connected to server"
        assert re.search(r'\bnginx\b', resp.info()['Server']), "http server is nginx"
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
        '-d': 'exists',
        '-r': 'has read perms',
        '-w': 'has write perms',
        '-x': 'has search perms',
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
        assert s.run(cmd).succeeded, "{0}/web/public/test.html created".format(home)
        url = "http://" + s.ip + "/test.html"
        resp = urllib.urlopen(url)
        assert resp.getcode() == 200, "server answered 200 OK for " + url
        assert resp.read() == data, "server returned content of test.html"
    except Exception as e:
        assert False, str(e)

def test_get_noext(s):
    try:
        url = "http://" + s.ip + "/"
        resp = urllib.urlopen(url)
        assert resp.getcode() == 404, "server answered 404 NotFound for " + url
    except Exception as e:
        assert False, str(e)

def test_get_upload(s):
    try:
        data = str(random.random())
        cmd = 'echo -n {0} > {1}/web/uploads/test.html'.format(data, home)
        assert s.run(cmd).succeeded, "{0}/web/uploads/test.html created".format(home)
        url = "http://" + s.ip + "/uploads/test.html"
        resp = urllib.urlopen(url)
        assert resp.getcode() == 200, "server answered 200 OK for " + url
        assert resp.read() == data, "server returned content of uploads/test.html"
    except Exception as e:
        raise
        assert False, str(e)


'''
sudo apt-get update
sudo apt-get install -y nginx
sudo apt-get install -y curl
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
'''
