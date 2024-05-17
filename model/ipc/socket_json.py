import json


def send_json(sock, data):
    try:
        serialized = json.dumps(data).encode()
    except (TypeError, ValueError):
        raise RuntimeError('You can only send JSON-serializable data')
    sock.sendall(serialized)


def recv_json(sock):
    data = sock.recv(1024).decode()
    try:
        deserialized = json.loads(data)
    except (TypeError, ValueError):
        raise RuntimeError(f'Data received ({data}) was not in JSON format')
    return deserialized
