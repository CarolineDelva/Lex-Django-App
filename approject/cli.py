import numpy as np 
from pset_3.data import load_vectors, load_words, load_data
from pset_3.embedding import WordEmbedding
import argparse

# Arguments to run via console.
parser = argparse.ArgumentParser(
    description='Get the embeddings for ...')
parser.add_argument("-w", '--words',
                    type=str,  required=True,
                    help='word list (*.txt)')
parser.add_argument("-e", '--embeddings',
                    type=str,  # required=True,
                    help='Word to vec embeddings (*.npz.gz)')
parser.add_argument("-p", '--project',
                    type=str,  # required=True,
                    help='File with ... (*.parquet)')

args = parser.parse_args()


def main(args=None):
    embedding = WordEmbedding.from_files(args.words, args.embeddings)

    # read in the hashed student data
    data = load_data(args.project)

    # create the vector representation for each survey entry
    # Note: this result will be a Series object preserving the
    # index with vectors inside
    embeddings = data['project'].apply(embedding.embed_document)
    return embeddings
    
    
if __name__=='__main__':
    main(args)
    