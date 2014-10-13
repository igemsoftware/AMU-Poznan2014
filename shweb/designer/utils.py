import requests
import urllib
import json
from django.conf import settings


class ShmirDesigner(object):
    server_url = settings.SHMIR_API_ADDRESS.rstrip('/')

    @classmethod
    def _process(cls, method, url, *args, **kwargs):
        request_url = "%s/%s" % (cls.server_url, url.strip('/'))

        for arg in args:
            request_url += '/%s' % arg

        request_url += '?' + urllib.urlencode(kwargs) if kwargs else ''
        action = getattr(requests, method.lower())
        response = action(request_url)
        return json.loads(response.content)

    @classmethod
    def mfold(cls, data):
        response = cls._process('get', 'mfold', data)
        return response.get('task_id')

    @classmethod
    def mfold_status(cls, task_id):
        response = cls._process('get', 'mfold', 'status', task_id)
        return response.get('status')

    @classmethod
    def from_transcript_create(cls, data):
        response = cls._process('get', 'from_transcript', **data)
        return response.get('task_id')

    @classmethod
    def structures(cls):
        structures = cls._process('get', 'structures')
        templates = structures.get('templates', []) + ['all']
        return sorted(templates)
