from src.Infrastructure import FileParser
from src.Application import QuerySearcher
import os
from dotenv import load_dotenv


class SearcherFactory:
    def create(self):
        load_dotenv()
        vllm_folder = os.getenv('RAW_DIR')
        processed_folder = os.getenv('PROCESSED_DIR')
        file_parser = FileParser(vllm_folder, processed_folder)
        query_searcher = QuerySearcher(file_parser)
        return query_searcher
