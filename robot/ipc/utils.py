import subprocess


def _guess_encoding(byte_sequence: bytes) -> str | None:
    """
    Пытается угадать, в какой кодировке записана последовательность байтов.
    В случае, если определить кодировку не получается, возвращается `None`.
    """
    variants = [
        'ascii',
        'cp866',
        'cp1251',
        'utf_8',
    ]

    for encoding in variants:
        try:
            byte_sequence.decode(encoding)
            return encoding
        except:
            pass

    return None


class CannotDetectEncodingError(Exception):
    pass


def is_process_alive(pid: int) -> bool:
    """
    Проверяет, что процесс с заданным PID существует.
    Работает только в Windows.
    """
    result = subprocess.check_output(
        ["tasklist", "/nh", "/fi", f"pid eq {pid}"],
        creationflags=subprocess.CREATE_NO_WINDOW,
        )
    
    encoding = _guess_encoding(result)
    if encoding is None:
        raise CannotDetectEncodingError

    result = result.decode(encoding)
    return str(pid) in result


def kill_process(pid: int) -> None:
    """
    Завершает процесс с заданным PID.
    Работает только в Windows.
    """
    subprocess.check_output(
        ["taskkill", "/f", "/pid", str(pid), "/t"],
        creationflags=subprocess.CREATE_NO_WINDOW,
        )
