"""
Handlers

"""

import operator

from flask import (
    jsonify,
    send_file
)

from shmir import app
from shmir.celery import (
    get_async_result,
    # get_group_async_result
)
from shmir.designer.design import design_and_score
from shmir.mfold import delegate_mfold
from shmir.utils import get_zip_path


@app.route('/mfold/status/<task_id>')
def mfold_task_status(task_id):
    return jsonify(get_async_result(delegate_mfold, task_id, only_status=True))


@app.route('/mfold/result/<task_id>')
def mfold_files(task_id):
    status = get_async_result(delegate_mfold, task_id, only_status=True)
    if status['status'] == 'fail':
        return jsonify({
            'status': 'error', 'error': 'Task is not ready or has failed'
        })

    zip_file = get_zip_path(task_id)

    try:
        return send_file(zip_file)
    except IOError:
        return jsonify({
            'status': 'error', 'error': 'File does not exist'
        })


@app.route('/mfold/<data>')
def mfold_data_handler(data):
    resource = delegate_mfold.apply_async(args=(data.upper(),), queue='main')
    return jsonify({'task_id': resource.task_id})


@app.route('/designer/status/<task_id>')
def designer_task_status(task_id):
    return jsonify(get_async_result(
        design_and_score, task_id, only_status=True)
    )


@app.route('/designer/result/<task_id>')
def designer_task_result(task_id):
    result = get_async_result(design_and_score, task_id)

    # result['data'] = [
    #     elem for elem in sorted(
    #         result['data'], key=operator.itemgetter(0), reverse=True
    #     ) if elem[0] > 60
    # ][:3]

    return jsonify(result)


@app.route('/designer/<data>')
def design_handler(data):
    # tasks_id = design_and_score(data.upper())
    # return jsonify({'task_id': tasks_id})
    resource = design_and_score.apply_async(args=(data.upper(),), queue='main')
    return jsonify({'task_id': resource.task_id})
