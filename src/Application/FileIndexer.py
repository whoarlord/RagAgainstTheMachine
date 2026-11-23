from src.Infrastructure import FileReader

class FileIndexer:
    def __init__(self, file_reader: FileReader, file_saver: FIleSaver):
        self.file_reader = file_reader

    def create_json(self, )

    def index_file(self, max_chunk_size: int, files_path: list):
        for file in files_path:
            file_text = self.file_reader.get_file(file)
            