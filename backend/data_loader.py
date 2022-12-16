# from beir.datasets.data_loader import GenericDataLoader
from argparse import ArgumentParser
from backend.bm25_search import Searcher
from pathlib import Path
import os
import logging
from tqdm import tqdm
import json

logger = logging.getLogger(__name__)

class GenericDataLoader:
    def __init__(self, data_folder: str = None, prefix: str = None, corpus_file: str = "corpus.jsonl", query_file: str = "queries.jsonl", 
                 qrels_folder: str = "qrels", qrels_file: str = ""):
        self.corpus = {}
        self.queries = {}
        self.qrels = {}
        
        if prefix:
            query_file = prefix + "-" + query_file
            qrels_folder = prefix + "-" + qrels_folder

        self.corpus_file = os.path.join(data_folder, corpus_file) if data_folder else corpus_file
        self.query_file = os.path.join(data_folder, query_file) if data_folder else query_file
        self.qrels_folder = os.path.join(data_folder, qrels_folder) if data_folder else None
        self.qrels_file = qrels_file
    
    def _load_corpus(self):
        num_lines = sum(1 for i in open(self.corpus_file, 'rb'))
        with open(self.corpus_file, encoding='utf8') as fIn:
            for line in tqdm(fIn, total=num_lines):
                line = json.loads(line)
                self.corpus[line.get("_id")] = {
                    "text": line.get("text"),
                    "title": line.get("title"),
                }
    
    def load_corpus(self):
        if not len(self.corpus):
            logger.info("Loading Corpus...")
            self._load_corpus()
            logger.info("Loaded %d Documents.", len(self.corpus))
            logger.info("Doc Example: %s", list(self.corpus.values())[0])

        return self.corpus

def main(args):
    data_path = args.data_path
    corpus = GenericDataLoader(data_path).load_corpus()
    
    searcher = Searcher("http://elasticsearch:9200", args.index_name)
    searcher.delete_index()
    searcher.create_index()
    searcher.add_corpus_to_index(corpus)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--data_path", type=Path, default="./backend/datasets/trec-covid")
    parser.add_argument("--index_name", type=str, default="main_index")
    args = parser.parse_args()
    
    main(args)