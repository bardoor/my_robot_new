from pathlib import Path


def file_exists(file_name: str | Path) -> bool:
    return Path(file_name).exists()


def get_ext(file_name: str | Path) -> str:
    return Path(file_name).suffix[1:]


def add_extension_if_not_present(file_name: str | Path, ext: str) -> Path:
    if get_ext(file_name):
        return file_name

    if not ext.startswith('.'): ext = f'.{ext}'

    if isinstance(file_name, str) and not file_name.endswith(ext):
        file_name = f'{file_name}{ext}'
    elif isinstance(file_name, Path) and file_name.suffix != ext:
        file_name = f'{file_name}{ext}'

    return file_name


class FieldFileNotFoundError(Exception):
    pass


class NotFieldFileError(Exception):
    pass
