from src.Infrastructure import FileReader, FileSaver
from src.Domain import Chunk
import pathlib
from tqdm import tqdm
import time
import ast


class FileIndexer:
    def __init__(self, file_reader: FileReader, file_saver: FileSaver):
        self.file_reader = file_reader
        self.file_saver = file_saver

    def write_in_file(self, chunk: Chunk):
        len = self.file_saver.concat_text(
            chunk.file_path, chunk.model_dump_json())
        chunk_characters = chunk.end - chunk.start
        """ if len != chunk_characters:
            raise ValueError(f"The saved characters: {len} aren't the same as the chunk characters {chunk_characters}") """

    def index_file(self, max_chunk_size: int, file: str):
        file_text = self.file_reader.get_file(file)
        start = 0
        while start < len(file_text):
            end = start + max_chunk_size
            text = file_text[start:end]
            yield Chunk(file_path=file, start=start, end=start + len(text), text=text)
            start = end
                
    def process_files(self, max_chunk_size: int, files_path: list[str] = []):
        self.file_saver.delete_folder_files()
        if (len(files_path) == 0):
            files_path = self.file_reader.list_files()
        for file in tqdm(files_path, desc="Random Iteration"):
            chunks = self.get_chunks_by_file(max_chunk_size, file)
            self.file_saver.save_json(file, chunks)
            
    def get_chunks_by_file(self, max_chunk_size: int, file: str):
        if file.endswith('.py'):
            chunks = [chunk.model_dump() for chunk in self.index_python_file(max_chunk_size, file)]
        elif file.endswith('.md'):
            chunks = [chunk.model_dump() for chunk in self.index_file(max_chunk_size, file)]
        else:
            chunks = [chunk.model_dump() for chunk in self.index_file(max_chunk_size, file)]
        return chunks
        
    def index_python_file(self, max_chunk_size: int, file: str):
        file_text = self.file_reader.get_file(file)
        line_starts = [0]
        for line in file_text.splitlines(keepends=True):
            line_starts.append(line_starts[-1] + len(line))
        
        tree = ast.parse(file_text)
        for node in tree.body:
            # print(type(node).__name__)
            if (type(node).__name__ == 'FunctionDef'
                or type(node).__name__ == 'AsyncFunctionDef'
                or type(node).__name__ == 'ClassDef'):
                start = line_starts[node.lineno - 1]
                end_char = line_starts[node.end_lineno]
                end = min(start + max_chunk_size, end_char)
                print(f"file: {file}, start: {start}, end {end}")
                while start < end_char:
                    text = file_text[start:end]
                    yield Chunk(file_path=file, start=start, end=start + len(text), text=text)
                    start = end
                    end = min(start + max_chunk_size, end_char)