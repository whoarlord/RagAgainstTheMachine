import pathlib
import json
import shutil
from src.Domain.Models import Chunk


class FileParser:
    def __init__(self, raw_folder: str, processed_folder: str):
        path = pathlib.Path(raw_folder)
        if (not path.exists()):
            raise FileNotFoundError(f"The folder doesn't exist: {raw_folder}")
        if not path.is_dir():
            raise NotADirectoryError(f"Is not a folder: {raw_folder}")
        self.raw_path = path
        path = pathlib.Path(processed_folder)
        if (not path.exists()):
            raise FileNotFoundError(
                f"The folder doesn't exist:{processed_folder}")
        if not path.is_dir():
            raise NotADirectoryError(f"Is not a folder: {processed_folder}")
        self.processed_path = path

    def _save_path(self, file_path: str) -> pathlib.Path:
        base = self.processed_path.resolve()
        path = (base / file_path).resolve()

        if not path.is_relative_to(base):
            raise ValueError(f"Path escapes the docs folder: {file_path}")

        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    def save_text(self, file_path: str, data: str) -> int:
        base = self.processed_path.resolve()
        path = (base / file_path).resolve()

        if not path.is_relative_to(base):
            raise ValueError(f"Path escapes the docs folder: {file_path}")
        if not path.is_file():
            raise FileNotFoundError(f"The file doesn't exist: {file_path}")

        return path.write_text(data, encoding="utf-8")

    def concat_text(self, file_path: str, data: str):
        base = self.processed_path.resolve()
        path = (base / file_path).resolve()

        if not path.is_relative_to(base):
            raise ValueError(f"Path escapes the output folder: {file_path}")

        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as f:
            return f.write(data)

    def append_jsonl(self, file_path: str, items: list | dict) -> None:
        path = self._save_path(file_path)
        with path.open("a", encoding="utf-8") as f:
            if (isinstance(items, list)):
                for item in items:
                    f.write(json.dumps(item, ensure_ascii=False) + "\n")
            elif (isinstance(items, dict)):
                f.write(json.dumps(items, ensure_ascii=False) + "\n")

    def delete_folder_files(self):
        if self.processed_path.exists():
            shutil.rmtree(self.processed_path)
        self.processed_path.mkdir(parents=True, exist_ok=True)

    def get_file(self, file_path: str) -> str:
        base = self.raw_path.resolve()
        path = (base / file_path).resolve()

        if not path.is_relative_to(base):
            raise ValueError(f"Path escapes the docs folder: {file_path}")
        if not path.is_file():
            raise FileNotFoundError(f"The file doesn't exist: {file_path}")

        return path.read_text(encoding="utf-8", errors="replace")

    def list_files(self) -> list[str]:
        root = self.raw_path
        out = []
        for pattern in ("vllm-0.10.1/**/*.md", "vllm-0.10.1/**/*.py"):
            out += [str(p.relative_to(root))
                    for p in root.glob(pattern) if p.is_file()]
        return sorted(out)

    def get_processed_file(self, file_path: str) -> list[Chunk]:
        base = self.processed_path.resolve()
        path = (base / file_path).resolve()
        with path.open(encoding="utf-8") as f:
            return [Chunk(**json.loads(line)) for line in f if line.strip()]
