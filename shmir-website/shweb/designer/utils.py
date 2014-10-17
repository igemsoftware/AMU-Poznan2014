"""
.. module:: shweb.designer
   :platform: Unix, Windows
   :synopsis: Module with usefull things for designer application.

"""
import requests
import urllib
import json
from django.conf import settings


class ShmirDesigner(object):
    """It's responsible for website <-> shmir API communication
    """
    server_url = settings.SHMIR_API_ADDRESS.rstrip('/')

    @classmethod
    def _process(cls, url, *args, **kwargs):
        """ Low level method responsible for making actual GET requests
        to "sh-miR designer" API.

        Args:
            url: URL of an REST method

        Returs:
            Python object loaded from server json response.
        """
        request_url = "%s/%s" % (cls.server_url, url.strip('/'))

        for arg in args:
            request_url += '/%s' % urllib.quote(arg)

        request_url += '?' + urllib.urlencode(kwargs) if kwargs else ''
        response = requests.get(request_url)
        return json.loads(response.content)

    @classmethod
    def build_pdf_url(cls, pdf_dirs):
        """Builds URL direct to mfold pdf files

        Args:
            pdf_dirs: pdf dirs returned from API results

        Returs:
            str concatenated with server url
        """
        return "%s/mfold/result/%s" % (cls.server_url, pdf_dirs)

    @classmethod
    def mfold(cls, data):
        """Method for mfold API call

        Args:
            data: str which should content one or two strands

        Returs:
            task_id from API
        """
        response = cls._process('mfold', data)
        return response.get('task_id')

    @classmethod
    def mfold_status(cls, task_id):
        """Method for mfold status API call

        Args:
            task_id: task id which status we're requesting for

        Returs:
            status "ok", "in progress", "fail" or "error"
        """
        response = cls._process('mfold', 'status', task_id)
        return response.get('status')

    @classmethod
    def mfold_result(cls, task_id):
        """Method for mfold result API call

        Args:
            task_id: task id which results we're requesting for

        Returs:
            python dict of results
        """
        response = cls._process('mfold', 'result', task_id)
        return response

    @classmethod
    def mfold_result_subdirs(cls, dir1, dir2):
        """Method for mfold subdirs API call

        Args:
            dir1: directory which contains input data from mfold request
            dir2: directory which contains task id
        Returs:
            response which could be zip or json
        """
        response = cls._process('mfold', 'result', dir1, dir2)
        return response

    @classmethod
    def from_sirna_create(cls, data):
        """Method for siRNA create API call

        Args:
            data: str which should content one or two siRNA strands

        Returs:
            task_id from API
        """
        sirna = data.pop('sirna')
        response = cls._process('from_sirna', sirna, **data)
        return response.get('task_id')

    @classmethod
    def from_sirna_status(cls, task_id):
        """Method for siRNA status API call

        Args:
            task_id: task id which status we're requesting for

        Returs:
            status "ok", "in progress", "fail" or "error"
        """
        response = cls._process('from_sirna', 'status', task_id)
        return response

    @classmethod
    def from_sirna_result(cls, task_id):
        """Method for siRNA result API call

        Args:
            task_id: task id which results we're requesting for

        Returs:
            python dict of results
        """
        response = cls._process('from_sirna', 'result', task_id)
        return response

    @classmethod
    def from_transcript_create(cls, data):
        """Method for from_transcript create API call

        Args:
            data: iterable which contains all parameters like 'transcript', 'min_gc',
                'max_gc', 'max_offtarget', 'mirna_name', 'stymulators'

        Returs:
            task_id from API
        """
        transcript = data.pop('transcript')
        response = cls._process('from_transcript', transcript, **data)
        return response.get('task_id')

    @classmethod
    def from_transcript_status(cls, task_id):
        """Method for from_transcript status API call

        Args:
            task_id: task id which status we're requesting for

        Returs:
            status "ok", "in progress", "fail" or "error"
        """
        response = cls._process('from_transcript', 'status', task_id)
        return response

    @classmethod
    def from_transcript_result(cls, task_id):
        """Method for from_transcript result API call

        Args:
            task_id: task id which results we're requesting for

        Returs:
            python dict of results
        """
        response = cls._process('from_transcript', 'result', task_id)
        return response

    @classmethod
    def structures(cls):
        """Method for getting all currently available miR structures in API database

        Returs:
            sorted list of miR structures
        """
        structures = cls._process('structures')
        templates = structures.get('templates', []) + ['all']
        return sorted(templates)
