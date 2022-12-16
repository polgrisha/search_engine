from flask import Flask, request
from flask_cors import CORS
from backend.bm25_search import Searcher
from backend.data_loader import GenericDataLoader
import os

DATA_PATH = "./backend/datasets/trec-covid"
INDEX_NAME = "main_index"
ELASTIC_HOST = "http://elasticsearch:9200"

app = Flask(__name__)
CORS(app)
searcher = Searcher(ELASTIC_HOST, INDEX_NAME)

@app.route('/')
def api_root():
    return 'My app'

@app.route("/search")
def search_autocomplete():
    query = request.args['q']
    res = searcher.search(query, 100)
    return res

if __name__ == "__main__":
    # corpus = GenericDataLoader(DATA_PATH).load_corpus()
    # searcher.delete_index()
    # searcher.create_index()
    # searcher.add_corpus_to_index(corpus)
    
    app.run(host='0.0.0.0', debug=True)