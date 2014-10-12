"""
.. module:: utils
    :synopsis: provides helpful functions to run client
"""
import requests
import time
import zipfile
import os
from settings import METHODS


def get_request(method, data, **kwargs):
    req = requests.get(METHODS[method].format(data), **kwargs)
    if req.status_code == 200:
        return req


def get_json(method, data, **kwargs):
    return get_request(method, data, **kwargs).json()


def creator(method, data, **kwargs):
    return get_json(method, data, **kwargs)["task_id"]


def checker(method, data, only_status=True):
    if only_status:
        return get_json(method, data)['status']
    return get_json(method, data)


def unzip(filename, path="."):
    with zipfile.ZipFile(filename) as zip_file:
        if not os.path.exists(path):
            os.makedirs(path)
        zip_file.extractall(path=path)


def change_ttw(x):
    if x < 15:
        return 0
    elif x > 42:
        return 120
    return 1.2 ** (x - 15)


def wait_until_task(task_id, checker, getter, *args):

    ttw = 0.5
    counter = 0

    status = checker(task_id)
    while status not in ["ok", "fail", "error"]:
        status = checker(task_id)
        time.sleep(ttw)
        counter += 1
        ttw += change_ttw(counter)

    if status in ["fail", "error"]:
        data = checker(task_id, only_status=False)
        print "{}: {}".format(data['status'], data['data']['result'])
        return

    return getter(task_id, *args)
