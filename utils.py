"""
.. module:: utils
    :synopsis: provides helpful functions to run client
"""
import requests
import time
import zipfile
from settings import METHODS


def get_request(method, data):
    req = requests.get(METHODS[method].format(data))
    if req.status_code == 200:
        return req


def get_json(method, data, key):
    return get_request(method, data).json()[key]


def creator(method, data):
    return get_json(method, data, "task_id")


def checker(method, data):
    return get_json(method, data, "status")


def unzip(filename):
    with zipfile.ZipFile(filename) as zip_file:
        zip_file.extractall(path=".")


def change_ttw(x):
    if x < 15:
        return 0
    elif x > 42:
        return 120
    return 1.2 ** (x - 15)


def wait_until_task(creator, create_data,
                    checker,
                    getter, get_data=()):

    ttw = 0.5
    counter = 0

    task_id = creator(create_data)
    while checker(task_id) != "ok":
        time.sleep(ttw)
        ttw += change_ttw(counter)

    return getter(task_id, *get_data)
