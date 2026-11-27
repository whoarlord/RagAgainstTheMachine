from src.Infrastructure import IndexerFactory, SearcherFactory

class CLI:
    def index(self, max_chunk_size: int):
        factory = IndexerFactory()
        indexer = factory.createIndexer()
        indexer.process_files(max_chunk_size)

    def search(self, query: str, k: int):
        factory = SearcherFactory()
        searcher = factory.create()
        searcher.search(query, k)

    def search_dataset(self, dataset_path: str, k: int, save_directory: str):
        pass

    def answer_dataset(self, student_search_results_path: str, save_directory: str):
        pass

    def evaluate(self, student_search_results_path: str, dataset_path: str):
        pass
