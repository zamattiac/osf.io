import json
import asyncio

import aiohttp


class _AioPretty:
    def __init__(self):
        self.request = None
        self.registry = {}
        self.calls = []


aiopretty = _AioPretty()


def make_call(**kwargs):
    return kwargs


@asyncio.coroutine
def process_request(**kwargs):
    """Process request options as if the request was actually executed."""
    data = kwargs.get('data')
    if isinstance(data, asyncio.StreamReader):
        yield from data.read()


@asyncio.coroutine
def fake_request(method, uri, **kwargs):
    try:
        options = aiopretty.registry[(method, uri)]
    except KeyError:
        raise Exception('No URLs matching {method} {uri}. Not making request. Go fix your test.'.format(**locals()))

    yield from process_request(**kwargs)
    aiopretty.calls.append(make_call(method=method, uri=uri, **kwargs))
    mock_response = aiohttp.client.ClientResponse(method, uri)
    mock_response._content = options.get('body', 'aiopretty')
    mock_response.headers = aiohttp.client.CaseInsensitiveMultiDict(options.get('headers', {}))
    mock_response.status = options.get('status', 200)
    return mock_response


def register_uri(method, uri, **options):
    aiopretty.registry[(method, uri)] = options


def register_json_uri(method, uri, **options):
    body = json.dumps(options.pop('body', None)).encode('utf-8')
    headers = {'Content-Type': 'application/json'}
    headers.update(options.pop('headers', {}))
    register_uri(method, uri, body=body, headers=headers, **options)


def activate():
    aiohttp.request, aiopretty.request = fake_request, aiohttp.request


def deactivate():
    aiohttp.request, aiopretty.request = aiopretty.request, None


def clear():
    aiopretty.registry = {}


def compare_call(first, second):
    for key, value in first.items():
        if second.get(key) != value:
            return False
    return True


def has_call(**kwargs):
    for call in aiopretty.calls:
        if compare_call(kwargs, call):
            return True
    return False