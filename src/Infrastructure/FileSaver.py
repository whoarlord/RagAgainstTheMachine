import pathlib
import json
import shutil


class FileSaver:
    def __init__(self, docs_folder: str):
        path = pathlib.Path(docs_folder)
        if (not path.exists()):
            raise FileNotFoundError(f"The folder doesn't exist: {docs_folder}")
        if not path.is_dir():
            raise NotADirectoryError(f"Is not a folder: {docs_folder}")
        self.folder_path = path

    def _save_path(self, file_path: str) -> pathlib.Path:
        base = self.folder_path.resolve()
        path = (base / file_path).resolve()

        if not path.is_relative_to(base):
            raise ValueError(f"Path escapes the docs folder: {file_path}")

        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    def save_text(self, file_path: str, data: str) -> int:
        base = self.folder_path.resolve()
        path = (base / file_path).resolve()

        if not path.is_relative_to(base):
            raise ValueError(f"Path escapes the docs folder: {file_path}")
        if not path.is_file():
            raise FileNotFoundError(f"The file doesn't exist: {file_path}")

        return path.write_text(data, encoding="utf-8")

    def concat_text(self, file_path: str, data: str):
        base = self.folder_path.resolve()
        path = (base / file_path).resolve()

        if not path.is_relative_to(base):
            raise ValueError(f"Path escapes the output folder: {file_path}")

        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as f:
            return f.write(data)
        
    def save_json(self, file_path: str, obj: any):
        path = self._save_path(file_path)
        with path.open("w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
            
    def delete_folder_files(self):
        if self.folder_path.exists():
            shutil.rmtree(self.folder_path)
        self.folder_path.mkdir(parents=True, exist_ok=True)