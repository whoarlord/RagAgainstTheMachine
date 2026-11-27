from src.Infrastructure.FileParser import FileParser


class QuerySearcher:
    def __init__(self, file_parser: FileParser):
        self.file_parser = file_parser

    def search(self, query: str, k: int):
        pass
