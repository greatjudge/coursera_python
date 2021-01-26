import argparse
import os
import tempfile
import json


def get_path():
    file_path = os.path.join(tempfile.gettempdir(), 'storage.data')
    return file_path


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--key", "--k", help="key for value")
    parser.add_argument("--value", "-v")
    return parser.parse_args()


def file_read(file_path):
    """
    read all JSON-data in file
    :return: dict
    """

    if not os.path.exists(file_path):
        return {}

    with open(file_path) as file:
        return json.load(file)


def get_list(file_path, key):
    """
    return list of values or empty list by key
    """

    data_map = file_read(file_path)
    data_map[key] = data_map.get(key, [])
    return data_map[key]


def file_write(file_path, data_map):
    with open(file_path, "w") as file:
        json.dump(data_map, file)


def put_data(file_path, key, value):
    """
    adds the value to the list by key
    """

    data_map = file_read(file_path)

    data_map[key] = data_map.get(key, [])
    data_map[key].append(value)

    file_write(file_path, data_map)


def execute_command(file_path, args):
    key = args.key
    value = args.value

    if value is None:
        print(*get_list(file_path, key), sep=", ")
    else:
        put_data(file_path, key, value)


def __main__():
    args = parse_args()
    file_path = get_path()
    execute_command(file_path, args)


if __name__ == "__main__":
    __main__()
