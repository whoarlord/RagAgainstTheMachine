import pathlib


class FileReader:
    def __init__(self, docs_folder: str):
        path = pathlib.Path(docs_folder)
        if (not path.exists()):
            raise FileNotFoundError(f"The folder doesn't exist: {docs_folder}")
        if not path.is_dir():
            raise NotADirectoryError(f"Is not a folder: {docs_folder}")
        self.folder_path = path

    def get_file(self, file_path: str) -> str:
        base = self.folder_path.resolve()
        path = (base / file_path).resolve()

        if not path.is_relative_to(base):
            raise ValueError(f"Path escapes the docs folder: {file_path}")
        if not path.is_file():
            raise FileNotFoundError(f"The file doesn't exist: {file_path}")

        return path.read_text(encoding="utf-8", errors="replace")

    def list_files(self) -> list[str]:
        root = self.folder_path
        out = []
        for pattern in ("vllm-0.10.1/**/*.md", "vllm-0.10.1/**/*.py"):
            out += [str(p.relative_to(root)) for p in root.glob(pattern) if p.is_file()]
        return sorted(out)