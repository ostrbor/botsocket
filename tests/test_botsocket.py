from botsocket.server import _parse_request, _run_command, _host_is_valid
import botsocket


def test_parse_command():
    assert b'GET' == _parse_request(b'GET something')

def test_run_command():
    assert b'RESULT' == _run_command(b'GET')

def test_host_is_valid(monkeypatch):
    HOST = '127.0.0.0'
    monkeypatch.setattr(botsocket.server, 'ALLOWED_HOST', HOST)
    assert _host_is_valid(HOST)


