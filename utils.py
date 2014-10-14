"""
.. module:: utils
    :synopsis: provides functions to handle requests,
        unzip file, generic creator, generic checker
"""
import requests
import time
import zipfile
import os
from settings import METHODS


def get_request(method, data, **kwargs):
    """Send http get request on url specified in settings

    Args:
        method: The name of method specified in settings
        data (str): String which will be concatenated with url
    Kwargs:
        **kwargs: Additional parameters used in requests

    Returns:
        request object
"""
    req = requests.get(METHODS[method].format(data), **kwargs)
    if req.status_code == 200:
        return req


def get_json(method, data, **kwargs):
    """Shortcut to get json from request

    Args:
        method: The name of method specified in settings
        data (str): String which will be concatenated with url
    Kwargs:
        **kwargs: Additional parameters used in requests

    Returns:
        dict object
    """
    return get_request(method, data, **kwargs).json()


def creator(method, data, **kwargs):
    """Generic function which create task and returns its id

    Args:
        method: The name of method specified in settings
        data (str): String which will be concatenated with url
    Kwargs:
        **kwargs: Additional parameters used in requests

    Returns:
        task_id (str): UUID4 task id
    """
    return get_json(method, data, **kwargs)["task_id"]


def checker(method, data, only_status=True):
    """Generic function which create task and returns its id

    Args:
        method: Name of method specified in settings
        data (str): String which will be concatenated with url
    Kwargs:
        only_status(bool): parameter to set up only status from json or whole json

    Returns:
        status (str): Status of task: "ok", "fail", "error"
        json (dict): Whole json data
    """

    if only_status:
        return get_json(method, data)['status']
    return get_json(method, data)


def unzip(filename, path="."):
    """Function to unzip file in specific path

    Args:
        filename: The name of file to unzip
        path: The directory in which this file should be unzipped

    Returns:
        None
    """
    with zipfile.ZipFile(filename) as zip_file:
        if not os.path.exists(path):
            os.makedirs(path)
        zip_file.extractall(path=path)


def change_ttw(x):
    """Math function which creates next time to wait (ttw)

    Args:
        x (int): number of checks

    Returns:
        time to wait
    """
    if x < 15:
        return 0
    elif x > 42:
        return 120
    return 1.2 ** (x - 15)


def wait_until_task(task_id, checker, getter, *args):
    """Function which waits until task is done and send output futher

    Args:
        task_id: Id of task which was given by RESTful API
        checker: Function which checks the status.
            Created via generic "checker" function
        getter: Function which gets results.
            Created via generic "getter" function
        *args: Other arguments used in getter function

    Returns:
        None if error
        Results from getter
    """

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
