"""
Funciones auxiliares de main.py


"""

def read_profile(filename):

    """
    INPUTS
    filename: str.

    OUTPUTS
    df: dataframe
    """

    import pandas as pd

    df = pd.read_csv(filename, index_col= )
