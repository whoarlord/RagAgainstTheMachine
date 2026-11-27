from src.Infrastructure import FileParser
from src.Domain import Chunk
from tqdm import tqdm
import ast
import re
from collections import Counter
import math


class FileIndexer:
    def __init__(self, file_parser: FileParser):
        self.file_parser = file_parser
        self.chunk_file = 'chunk.json'
        self.tokenized_file = 'tokenized.json'

    def index_file(self, max_chunk_size: int, file: str):
        file_text = self.file_parser.get_file(file)
        start = 0
        while start < len(file_text):
            end = start + max_chunk_size
            text = file_text[start:end]
            yield Chunk(file_path=file, start=start, end=start + len(text), text=text)
            start = end

    def process_files(self, max_chunk_size: int, files_path: list[str] = []):
        self.file_parser.delete_folder_files()
        if (len(files_path) == 0):
            files_path = self.file_parser.list_files()
        for file in tqdm(files_path, desc="Chunking"):
            chunks = self.get_chunks_by_file(max_chunk_size, file)
            self.file_parser.append_jsonl(self.chunk_file, chunks)

        chunks = self.file_parser.get_processed_file(self.chunk_file)
        doc_lengths = [len(re.findall(r'\w+', c.text.lower())) for c in chunks]
        avgdl = sum(doc_lengths) / len(doc_lengths)
        df = Counter()
        N = len(chunks)
        for chunk in chunks:
            tokens = re.findall(r'\w+', chunk.text.lower())
            df.update(set(tokens))
        for chunk in tqdm(chunks, desc="Tokenizing"):
            tokenized = self._bm_indexing(chunk, avgdl, N, df)
            self.file_parser.append_jsonl(self.tokenized_file, tokenized)

    def get_chunks_by_file(self, max_chunk_size: int, file: str):
        if file.endswith('.py'):
            chunks = [chunk.model_dump() for chunk in self.chunking_python_file(max_chunk_size, file)]
        elif file.endswith('.md'):
            chunks = [chunk.model_dump() for chunk in self.chunking_md_file(max_chunk_size, file)]
        else:
            chunks = [chunk.model_dump() for chunk in self.chunking_file(max_chunk_size, file)]
        return chunks

    def chunking_md_file(self, max_chunk_size: int, file: str):
        file_text = self.file_parser.get_file(file)
        chunks = []
        i = 0
        matches = list(re.finditer(r'^#{1,6}\s+(.*)$', file_text, re.MULTILINE))
        for i, match in enumerate(matches):
            start = match.start()
            last = matches[i + 1].start() if i + 1 < len(matches) else len(file_text)
            end = min(start + max_chunk_size, last)
            chunks.extend(self._iterate_over_char(file_text, start, end, last, max_chunk_size, file))
        return chunks
            
    def chunking_python_file(self, max_chunk_size: int, file: str):
        chunks = []
        file_text = self.file_parser.get_file(file)
        line_starts = [0]
        for line in file_text.splitlines(keepends=True):
            line_starts.append(line_starts[-1] + len(line))
        
        tree = ast.parse(file_text)
        for node in tree.body:
            if (type(node).__name__ == 'FunctionDef'
                or type(node).__name__ == 'AsyncFunctionDef'
                or type(node).__name__ == 'ClassDef'):
                start = line_starts[node.lineno - 1]
                last = line_starts[node.end_lineno]
                end = min(start + max_chunk_size, last)
                chunks.extend(self._iterate_over_char(file_text, start, end, last, max_chunk_size, file))
        return chunks

    @staticmethod
    def _iterate_over_char(file_text: str, start: int, end: int, last: int, max_chunk_size: int, file: str):
        while start < last:
            text = file_text[start:end]
            yield Chunk(file_path=file, start=start, end=start + len(text), text=text)
            start = end
            end = min(start + max_chunk_size, last)

    def _bm_indexing(self, chunk: Chunk, avgdl: float, N: int, df: Counter):
        text = chunk.text
        tokens = re.findall(r'\w+', text.lower())
        frecuencias = Counter(tokens)
        b = 0.75
        k1 = 1.5
        doc_len = len(tokens)
        tokenized = {}
        for word, freq in frecuencias.items():
            idf = math.log((N - df[word] + 0.5) / (df[word] + 0.5) + 1)
            tf = freq * (k1 + 1) / (freq + k1 * (1 - b + b * doc_len / avgdl))
            tokenized[word] = idf * tf
        return tokenized
