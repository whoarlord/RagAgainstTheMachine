from src.Infrastructure import FileParser
from src.Application import FileIndexer
import os
from dotenv import load_dotenv


class IndexerFactory:
    def createIndexer(self):
        load_dotenv()
        vllm_folder = os.getenv('RAW_DIR')
        processed_folder = os.getenv('PROCESSED_DIR')
        file_parser = FileParser(vllm_folder, processed_folder)
        file_indexer = FileIndexer(file_parser)
        return file_indexer
