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
