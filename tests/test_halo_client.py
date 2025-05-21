import json
import os
import sys
from types import SimpleNamespace
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from halo_client import HaloClient

class DummyResponse:
    def __init__(self, data=b"{}"):  # default empty json
        self._data = data
    def read(self):
        return self._data
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, tb):
        pass

def test_request_get(monkeypatch):
    captured = {}
    def fake_urlopen(req):
        captured['method'] = req.get_method()
        captured['url'] = req.full_url
        captured['headers'] = dict(req.headers)
        captured['data'] = req.data
        return DummyResponse(b'{"ok": true}')
    monkeypatch.setattr(urllib.request, 'urlopen', fake_urlopen)
    client = HaloClient('http://example', 'token')
    result = client._request('GET', '/test')
    assert result == {"ok": True}
    assert captured['method'] == 'GET'
    assert captured['url'] == 'http://example/test'
    assert captured['headers']['Authorization'] == 'Bearer token'
    # urllib may normalize header names to lower case internally
    headers = {k.lower(): v for k, v in captured['headers'].items()}
    assert headers['content-type'] == 'application/json'
    assert captured['data'] is None

def test_request_post_with_data(monkeypatch):
    captured = {}
    def fake_urlopen(req):
        captured['method'] = req.get_method()
        captured['url'] = req.full_url
        captured['headers'] = dict(req.headers)
        captured['data'] = req.data
        return DummyResponse(b'null')
    monkeypatch.setattr(urllib.request, 'urlopen', fake_urlopen)
    client = HaloClient('http://host', 'k')
    result = client._request('POST', '/path', {"foo": 1})
    assert result is None
    assert captured['method'] == 'POST'
    assert captured['url'] == 'http://host/path'
    body = json.loads(captured['data'].decode())
    assert body == {"foo": 1}

def test_get_status_calls_request(monkeypatch):
    called = {}
    def fake_request(method, path, data=None):
        called['args'] = (method, path, data)
        return {'status': 'ok'}
    client = HaloClient('h', 'k')
    monkeypatch.setattr(client, '_request', fake_request)
    result = client.get_status('123')
    assert result == {'status': 'ok'}
    assert called['args'] == ('GET', '/api/chargers/123/status', None)

def test_start_stop_calls(monkeypatch):
    calls = []
    def fake_request(method, path, data=None):
        calls.append((method, path, data))
    client = HaloClient('h', 'k')
    monkeypatch.setattr(client, '_request', fake_request)
    client.start_charging('42')
    client.stop_charging('42')
    assert calls == [
        ('POST', '/api/chargers/42/charge/start', None),
        ('POST', '/api/chargers/42/charge/stop', None)
    ]
