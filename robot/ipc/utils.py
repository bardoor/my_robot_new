import subprocess


def is_process_alive(pid: int) -> bool:
    """
    Проверяет, что процесс с заданным PID существует.
    Работает только в Windows.
    """
    result = subprocess.check_output(
        ["tasklist", "/nh", "/fi", f"pid eq {pid}"],
        creationflags=subprocess.CREATE_NO_WINDOW,
        ).decode()
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
