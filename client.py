import time
import socket


class ClientError(socket.error):
    """:except client error"""


class Client:
    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout

        try:
            self.client_socket = socket.create_connection((host, port))
            self.client_socket.settimeout(timeout)
        except socket.error as err:
            print("Error connection:", err)

    def put(self, name_of_metric, num, timestamp=None):
        if timestamp is None:
            timestamp = int(time.time())

        try:
            self.client_socket.send(f"put {name_of_metric} {num} {timestamp}\n".encode())

            answer_string = self.client_socket.recv(1024)
            self.parse_to_map(answer_string.decode())
        except Exception:
            raise ClientError()

    @staticmethod
    def deleting_empty_strings(data_list):
        while data_list.count("") > 0:
            data_list.remove("")

    @staticmethod
    def parse_to_map(data_string):
        data_list = data_string.split('\n')

        if data_list[0] != 'ok':
            raise ClientError()

        del data_list[0]
        Client.deleting_empty_strings(data_list)

        if not data_list:
            return {}

        data_map = dict()
        for string in data_list:
            property_list = string.split()
            data_map[property_list[0]] = data_map.get(property_list[0], list())
            data_map[property_list[0]].append((int(property_list[2]), float(property_list[1])))

        for key in data_map:
            data_map[key].sort()

        return data_map

    def get(self, name_of_metric):
        try:
            query_string = f"get {name_of_metric}\n"
            self.client_socket.send(query_string.encode())

            data_string = self.client_socket.recv(1024)
            data_map = self.parse_to_map(data_string.decode())

            return data_map
        except Exception:
            raise ClientError()

    def close(self):
        try:
            self.client_socket.close()
        except socket.error as err:
            raise ClientError("Error close:", err)

