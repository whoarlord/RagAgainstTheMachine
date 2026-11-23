import pathlib


class FileSaver:
    def __init__(self, docs_folder: str):
        path = pathlib.Path(docs_folder)
        if (not path.exists()):
            raise FileNotFoundError(f"The folder doesn't exist: {docs_folder}")
        if not path.is_dir():
            raise NotADirectoryError(f"Is not a folder: {docs_folder}")
        self.folder_path = path

    def save_text(self, file_path: str, data) -> int:
        base = self.folder_path.resolve()
        path = (base / file_path).resolve()

        if not path.is_relative_to(base):
            raise ValueError(f"Path escapes the docs folder: {file_path}")
        if not path.is_file():
            raise FileNotFoundError(f"The file doesn't exist: {file_path}")

        return path.write_text(data, encoding="utf-8")
