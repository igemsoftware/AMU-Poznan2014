#!/usr/bin/env python

import argparse
import os
import shutil
from utils import (
    unzip,
    get_request,
    get_json,
    creator,
    checker,
    wait_until_task,
)


# mfold
def mfold_result(task_id, zipname="now.zip", path="./results/mfold/", verbose=True):
    req = get_request("mfold_result", task_id)
    with open(zipname, "wb") as f:
        for chunk in req.iter_content():
            f.write(chunk)
    unzip(zipname, path)
    os.remove(zipname)

    if verbose:
        print("Result under: {}/".format(path + task_id))


def mfold(sequence):
    return wait_until_task(
        creator("mfold_create", sequence),
        lambda task_id, **kwargs: checker("mfold_check", task_id, **kwargs),
        mfold_result
    )


# from sirna
def from_sirna_result(task_id):
    data = get_json("from_sirna_result", task_id)['data']

    path = "./results/sirna/{}/".format(task_id)
    print("Results under: {}".format(path))

    for no, (points, shmir, name, mfold_id) in enumerate(data['result']):
        mfold_result(mfold_id, path=path, verbose=False)
        new_path = path + name
        os.rename(path + mfold_id, new_path)
        print("{}: name: {}, score: {}, pdf: {}\n   result: {}".format(
            no, name, points, new_path, shmir
        ))


def from_sirna(sequences):
    return wait_until_task(
        creator("from_sirna_create", sequences),
        lambda task_id, **kwargs: checker("from_sirna_check", task_id, **kwargs),
        from_sirna_result
    )


# from transcript
def from_transcript_result(task_id):
    data = get_json("from_transcript_result", task_id)['data']

    path = "./results/transcript/{}/".format(task_id)
    print("Results under: {}".format(path))

    result_string = "{}: backbone: {}, score: {}, sequence: {}\n pdf: {}\n result: {}"
    for no, result in enumerate(data['result']):
        mfold_result(result['pdf'], path=path, verbose=False)
        new_path = path + result['backbone']

        if not os.path.exists(new_path):
            os.makedirs(new_path)

        subtask_id = result['pdf'].split("/")[-1]
        shutil.move(path + subtask_id, new_path)

        print(result_string.format(
            no,
            result['backbone'],
            result['score'],
            result['sequence'],
            os.path.join(new_path, subtask_id),
            result['sh_mir']
        ))


def from_transcript(transcript, params):
    return wait_until_task(
        creator("from_transcript_create", transcript, params=params),
        lambda task_id, **kwargs: checker("from_transcript_check", task_id, **kwargs),
        from_transcript_result
    )


if __name__ == '__main__':
    mfold_help = "Mfold option folds sequence via mfold"
    from_sirna_help = "From sirna option creates shmirs from sirna"
    from_transcript_help = "From transcript option creates shmirs from transcript"

    parser = argparse.ArgumentParser(prog="sh-miR client")
    subparsers = parser.add_subparsers(dest="parser")
    mfold_parser = subparsers.add_parser(
        "mfold",
        help=mfold_help,
    )
    mfold_parser.add_argument('sequence', type=str)

    sirna_parser = subparsers.add_parser(
        "from_sirna",
        help=from_sirna_help,
    )
    sirna_parser.add_argument('sequences', nargs="*", type=str)

    transcript_parser = subparsers.add_parser(
        "from_transcript",
        help=from_transcript_help
    )
    transcript_parser.add_argument("transcript", type=str)
    transcript_parser.add_argument("-mingc", "--min_gc", type=int)
    transcript_parser.add_argument("-maxgc", "--max_gc", type=int)
    transcript_parser.add_argument("-maxoff", "--max_offtarget", type=int)
    transcript_parser.add_argument("-mirna", "--mirna_name", type=str)
    transcript_parser.add_argument("-stm", "--stymulators", type=str)

    args = parser.parse_args()
    if args.parser == "from_sirna":
        if len(args.sequences) > 2:
            parser.error("from siRNA option needs 1 or 2 sequences")
        from_sirna(" ".join(args.sequences))

    elif args.parser == 'mfold':
        mfold(args.sequence)

    else:
        args_dict = dict(args._get_kwargs())
        for key in ['transcript', 'parser']:
            del args_dict[key]
        from_transcript(args.transcript, args_dict)
