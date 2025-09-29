import logging
from abc import ABC, abstractmethod
from typing import Union
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

class DataStrategy(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def handle_data(self, df:pd.DataFrame) -> Union[pd.DataFrame, pd.Series]:
        pass

    
class PreprocessingStrategy(DataStrategy):

    def handle_data(self, df:pd.DataFrame) -> Union[pd.DataFrame, pd.Series]:
        """
        

        Args:
            df (pd.DataFrame): _description_

        Returns:
            Union[pd.DataFrame, pd.Series]: _description_
        """

        try:
            data = df.
            return data