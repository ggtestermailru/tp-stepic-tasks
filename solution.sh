#!/bin/bash
rm -rf /home/box/web

# layout
mkdir -p /home/box/web/public
mkdir -p /home/box/web/public/js
mkdir -p /home/box/web/public/css
mkdir -p /home/box/web/public/img
mkdir -p /home/box/web/uploads/
mkdir -p /home/box/web/etc/

# nginx configuration
cat > /home/box/web/etc/nginx.conf <<EOC
server {
    listen 80 default_server;
    location /hello/ {
        proxy_pass http://127.0.0.1:8080/;
    }
    location / {
        proxy_pass http://127.0.0.1:8000/;
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

# mysql database
sudo /etc/init.d/mysql restart
mysql -uroot -e 'drop database test'
mysql -uroot -e 'drop user test'
mysql -uroot -e "create database test character set 'UTF8';"
mysql -uroot -e "grant all privileges on test.* to 'test'@'%' identified by 'test';"

# demo wsgi application
cat > /home/box/web/hello.py <<EOC
def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    qs = environ.get('QUERY_STRING', '')
    for w in qs.split('&'):
        yield w + '\n'
EOC

cat > /home/box/web/etc/hello <<EOC
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
sudo unlink /etc/gunicorn.d/hello
sudo ln -s /home/box/web/etc/hello /etc/gunicorn.d/hello

# djago gunicorn
cat > /home/box/web/etc/django <<EOC
CONFIG = {
    'working_dir': '/home/box/web/ask',
    'args': (
        '--bind=0.0.0.0:8000',
        '--workers=3',
        '--timeout=60',
        'ask.wsgi:application',
    ),
}
EOC
sudo unlink /etc/gunicorn.d/django
sudo ln -s /home/box/web/etc/django /etc/gunicorn.d/django

# init project
(cd /home/box/web && django-admin startproject ask)
(cd /home/box/web/ask && python2.7 manage.py startapp qa)

# project settings
cat >> /home/box/web/ask/ask/settings.py <<EOC
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test',
        'USER': 'test',
        'PASSWORD': 'test',
    }
}
INSTALLED_APPS = ('qa',) + INSTALLED_APPS
EOC
rm /home/box/web/ask/ask/settings.pyc   #  cache for some reason..

# models
cat > /home/box/web/ask/qa/models.py <<EOC
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class ModelManager(models.Manager):
    def new(self):
        return self.order_by('-added_at')
    def hot(self):
        return self.order_by('-rating')

class Question(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    added_at = models.DateTimeField(default=datetime.now)
    author = models.ForeignKey(User)
    likes = models.ManyToManyField(User, related_name='liked_question_set')
    rating = models.IntegerField(default=0)

class Answer(models.Model):
    text = models.TextField()
    added_at = models.DateTimeField(default=datetime.now)
    question = models.ForeignKey(Question)
    author = models.ForeignKey(User)
EOC

# sync down
python /home/box/web/ask/manage.py syncdb --noinput

# urls.py
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

# views
cat > /home/box/web/ask/qa/views.py <<EOC
from django.shortcuts import render
from django.http import HttpResponse
def test(request, *args, **kwargs):
    return HttpResponse('OK')
EOC

sudo /etc/init.d/gunicorn restart
