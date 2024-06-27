from pathlib import Path
import sys
import subprocess
import shutil
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def run() -> None:
    '''
    Создает виртуальную среду, устанавливает в нее необходимые зависимости
    и запускает графическое окно робота. После чего, как только окно закрылось,
    отключает виртуальную среду
    '''
    venv = Path('venv')

    # Небольшая оптимизация: если папка с виртуальной средой
    # уже имеется, то она не создается
    if not (venv.exists() or venv.is_dir()):
        subprocess.run(
            f'py -m venv {venv}',
            check=True,
            shell=True,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )

    command = (
        f'.\\{venv}\\Scripts\\activate.bat && '
        'py -m pip install -r requirements.txt && '
        'py -m robot.ipc.run_ui && '
        'deactivate'
    )
    
    try:
        subprocess.run(
            command,
            check=True,
            shell=True,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
        # Удаляем папку с виртуальной средой по окончании выполнения
        shutil.rmtree(venv, ignore_errors=True)
    except subprocess.CalledProcessError as ex:
        logger.error(f'Error: returned non-zero exit status {ex.returncode}')


if __name__ == "__main__":
    run()
