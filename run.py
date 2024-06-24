import argparse
from pathlib import Path
import os
import sys
import subprocess
import shutil
import logging


parser = argparse.ArgumentParser()
parser.add_argument('-s', '--silent', action='store_true', help="silent mode: no information printed except errors.")
parser.add_argument('-c', '--cleanup', action='store_true', help="erase venv directory when finished.")
args = parser.parse_args()


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
if args.silent:
    logging.disable(logging.CRITICAL)


venv_path = Path('venv')


def create_venv() -> None:
    if not (venv_path.is_dir() and venv_path.exists()):
        try:
            logger.info("No venv found, creating...")
            subprocess.run("py -m venv venv", check=True)
            logger.info("Created venv")
        except subprocess.CalledProcessError as ex:
            logger.error(f"Couldn't create venv")
            stderr_msg = ex.stderr.decode()
            if stderr_msg:
                logger.error(stderr_msg)
            os._exit(1)
    else:
        logger.info("Found existing venv")


def run_ui() -> None:
    RUN_COMMAND = (
        '.\\venv\\Scripts\\Activate.ps1;'
        'pip install -r requirements.txt;'
        'py -m robot.ipc.run_ui'
    )
    EXECUTABLE_SHELL = "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"

    try:
        result = subprocess.run(
            RUN_COMMAND,
            shell=True,
            executable=EXECUTABLE_SHELL,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
        if result.returncode != 0:
            os._exit(1)
    except subprocess.CalledProcessError as ex:
        logger.error(f"Couldn't run ui")
        stderr_msg = ex.stderr.decode()
        if stderr_msg:
            logger.error(stderr_msg)
    
    if args.cleanup:
        logger.info("Removing venv")
        shutil.rmtree(venv_path, ignore_errors=True)


if __name__ == "__main__":
    create_venv()
    run_ui()
