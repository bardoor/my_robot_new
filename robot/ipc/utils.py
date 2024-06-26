import subprocess
import re


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

    # Строка, которую возвращает tasklist имеет вид
    # browser.exe                   9392 Console                    1    17 980 K
    # Сжимаем все пробелы в один, после чего сплитим и изымаем PID
    result = re.sub(r'\s+', ' ', result.decode(encoding))
    parts = result.split()
    return str(pid) == parts[1]


def kill_process(pid: int) -> None:
    """
    Завершает процесс с заданным PID.
    Работает только в Windows.
    """
    subprocess.check_output(
        ["taskkill", "/f", "/pid", str(pid), "/t"],
        creationflags=subprocess.CREATE_NO_WINDOW,
        )
