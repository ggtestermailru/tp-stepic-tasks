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
