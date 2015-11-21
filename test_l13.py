import stepic_pytest.fixtures
# test_li13.py
import urllib
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import re
import random
import os
from contextlib import closing

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

def proxy(s, tst):
    cmd = 'PYTHONPATH={0}/web/ask/ python2.7 {0}/{1} 2>&1'.format(home, tst)
    res = s.run(cmd)
    if res.succeeded:
        msgs = re.findall('^(?!ERROR|FAIL)^\w+:\s*(.*)\s*$', res, flags=re.M)
        if len(msgs) > 0:
            assert False, "\n".join(msgs)
    else:
        raise Exception(res)

def test_init_data(s):
    proxy(s, 'server_l13.py TestInitData')

def test_last_question(s):
    try:
        url = "http://" + s.ip + "/"
        resp = urllib2.urlopen(url)
        assert resp is not None, "failed to connect to port nginx (port 80)"
        assert str(resp.getcode()) == '200', url + " didn't returned 200"
        with closing(resp) as resp2:
            body = resp2.read()
            assert re.search(r'\bquestion last\b', body), "last created question was not found on main page"
    except Exception as e:
        assert False, str(e)

def test_last_pagination(s):
    try:
        url = "http://" + s.ip + "/?page=2"
        resp = urllib2.urlopen(url)
        assert resp is not None, "failed to connect to port nginx (port 80)"
        assert str(resp.getcode()) == '200', url + " didn't returned 200"
        with closing(resp) as resp2:
            body = resp2.read()
            assert not re.search(r'\bquestion last\b', body), "last created question was erroneosly found on /?page=2. Does pagination work?"
    except Exception as e:
        assert False, str(e)

def test_popular_question(s):
    try:
        url = "http://" + s.ip + "/popular/"
        resp = urllib2.urlopen(url)
        assert resp is not None, "failed to connect to port nginx (port 80)"
        assert str(resp.getcode()) == '200', url + " didn't returned 200"
        with closing(resp) as resp2:
            body = resp2.read()
            assert re.search(r'\bquestion 28\b', body), "popular question (with rating 1028) was not found on /popular/ page"
            assert re.search(r'\bquestion 27\b', body), "popular question (with rating 1027) was not found on /popular/ page"
    except Exception as e:
        assert False, str(e)

def test_popular_question(s):
    try:
        url = "http://" + s.ip + "/popular/?page=2"
        resp = urllib2.urlopen(url)
        assert resp is not None, "failed to connect to port nginx (port 80)"
        assert str(resp.getcode()) == '200', url + " didn't returned 200"
        with closing(resp) as resp2:
            body = resp2.read()
            assert re.search(r'\bquestion 18\b', body), "popular question (with rating 1018) was not found on /popular/?page=2 page"
            assert re.search(r'\bquestion 17\b', body), "popular question (with rating 1017) was not found on /popular/?page=2 page"
            assert not re.search(r'\bquestion 28\b', body), "popular question (with rating 1028) was erroneosly found on first /popular page. Does pagination work?"
            assert not re.search(r'\bquestion 27\b', body), "popular question (with rating 1027) was erroneosly found on first /popular page. Does pagination work?"
    except Exception as e:
        assert False, str(e)

def test_question_page(s):
    try:
        url = "http://" + s.ip + "/question/3141592/"
        resp = urllib2.urlopen(url)
        assert resp is not None, "failed to connect to port nginx (port 80)"
        assert str(resp.getcode()) == '200', url + " didn't returned 200"
        with closing(resp) as resp2:
            body = resp2.read()
            assert re.search(r'\bquestion about pi\b', body), "question title is not found on question page " + url
            assert re.search(r'\banswer 5\b', body), "answer text is not found on question page " + url
    except Exception as e:
        assert False, str(e)

