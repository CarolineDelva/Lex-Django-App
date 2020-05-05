
import pandas as pd 
import numpy as np 
import pandas as pd 
import pyarrow.parquet as pq



def load_words(filename):
    """Load a file containing a list of words as a python list
    use case: data/words.txt
    :param str filename: path/name to file to load
    :rtype: list
    """
    # Opening the file and storing it into a variable
    file = open(filename, 'r+')
    # Using a list comprehension to read each line and store into a list
    words_list = [line.strip() for line in file.readlines()]
    # Closing the file 
    file.close()
    return words_list 
    

def load_vectors(filename):
#     """Loads a file containing word vectors to a python numpy array

#     use case: `data/vectors.npy.gz`
#     :param str filename:

#     :returns: 2D matrix with shape (m, n) where m is number of words in vocab
#         and n is the dimension of the embedding

#     :rtype: ndarray
#     """
#     ...
    # Loading the npz.gz file 
    filename = np.load(filename)
    # Turning the file into a 2D matrix 
    # Returning the numpy array
    return filename 

def load_data(filename):
#     """Load student response data in parquet format

#     use case: data/project.parquet
#     :param str filename:

#     :returns: dataframe indexed on a hashed github id
#     :rtype: DataFrame
#     """
#     # You will probably need to fill a few NA's and set/sort the index via
#     # pandas
#     ...
    
    # Reading the parquet file using pyarrow as engine
    filename = pd.read_parquet(filename, engine='pyarrow')
    # Sorting the user_id index in ascending way
    filename = filename.sort_index(ascending=True,)
    # Filling empty cell with string 'N/A'
    filename.fillna(value='N/A', inplace=True)
    # Return the filename as a dataframe
    return filename


