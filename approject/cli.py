import numpy as np 
from .data import load_vectors, load_words, load_data
from pset_3.embedding import WordEmbedding
from pset_3.cosinesimilarity import cosine_similarity
import argparse
from pset_3.io import atomic_write
import tempfile
from tempfile import TemporaryDirectory
import pandas as pd 
import pyarrow
import os, sys

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

parser.add_argument("-u", '--user',
                    type=str,  # required=True,
                    help='User Hash ... (str)')


args = parser.parse_args()



def main(args=None):
    # Appliyng the Wordembedding class to the files
    embedding = WordEmbedding.from_files(args.words, args.embeddings)
    # read in the hashed student data
    data = load_data(args.project)

    # create the vector representation for each survey entry
    # Note: this result will be a Series object preserving the
    # index with vectors inside
    embeddings = data['project'].apply(embedding.embed_document)
    # Assigning the user's hash to a variable
    user_emb_hash = embeddings.loc[args.user]
    # Calculating the distance between the user and the rest of the dataframe
    cos_similarity = embeddings.apply(lambda x: cosine_similarity(user_emb_hash, x))
    distances = 1 - cos_similarity
    # Creating a dataframe with the distances with the user_id
    distances.to_frame().columns = ['distance']
    distances = distances.to_frame()
    distances.columns = ['distance']

    #f = tempfile.NamedTemporaryFile()
   
    
    # utilize atomic_write to export results to data/...
    filename = "distance_to_peers.parquet"
    directory = "data/"
    if os.path.exists(filename):
        os.remove(filename)
    #filename = "data/distance_to_peers.parquet"
    with atomic_write(filename, as_file=False) as f:
        # Ensure you are ***only*** writing the index and distance!

        if not os.path.exists(directory):
            os.mkdir(directory)

        f = os.path.join(directory, filename)    


        distances.to_parquet(f)

       # atomic_write function checks if file exist and raises an FileExistsError
       # If file does not exist, print out a summary of yourself and the 4 closest students
       # reading project.parquet
        projectfile = pd.read_parquet(args.project, engine='pyarrow')
       #joining projectfile with distances
        five_friends = projectfile.join(distances).head(5) # join distance to project data, sort and select
       # Printing the summary of yourself and the 4 closest students 
       
        print(f"This is a summary of {args.user} and his closest friends: ")
        for friend, row in five_friends.iterrows():
            print("--------------------------------------------------------")
            print("With a user_id of: ", friend, row)

    return five_friends.distance.values
        

if __name__=='__main__':
    main(args)
    