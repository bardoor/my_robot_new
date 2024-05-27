import json


def send_json(sock, data):
    try:
        serialized = json.dumps(data).encode()
    except (TypeError, ValueError):
        raise RuntimeError('You can only send JSON-serializable data')
    sock.sendall(serialized)
    sock.sendall('\0'.encode())


def recv_json(sock):
    data = []
    while (byte := sock.recv(1)) != '\0'.encode():
        data.append(byte.decode())
    data = ''.join(data)
    try:
        deserialized = json.loads(data)
    except (TypeError, ValueError):
        raise RuntimeError(f'Data received ({data}) was not in JSON format')
    return deserialized
