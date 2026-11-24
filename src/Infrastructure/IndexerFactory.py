from src.Infrastructure import FileReader, FileSaver
from src.Application import FileIndexer
import os
from dotenv import load_dotenv

class IndexerFactory:
    def createIndexer(self):
        load_dotenv()
        vllm_folder = os.getenv('RAW_DIR')
        processed_folder = os.getenv('PROCESSED_DIR')
        
        
        file_reader = FileReader(vllm_folder)
        file_saver = FileSaver(processed_folder)
        file_indexer = FileIndexer(file_reader, file_saver)
        return file_indexer