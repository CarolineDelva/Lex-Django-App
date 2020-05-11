# Importing dependencies 
import numpy as np

"""
calculates the distance between two vectors 
takes the two vectors as arguments

"""


def cosine_similarity(vec1, vec2):
    # Getting the dot product of vectors a and b.
    dot_prod = np.dot(vec1, vec2)
    # Dividing dot_prod with the one of the eight different matrix norms 
    cos = dot_prod /(np.linalg.norm(vec1) * np.linalg.norm(vec2))
    # Returning the full funtion 
    return cos