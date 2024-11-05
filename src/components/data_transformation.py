import sys
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler,FunctionTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from src.constant import *
from src.logger import logging
from src.utils.main_utils import MainUtils
from src.exception import CustomException
from dataclasses import dataclass

@dataclass
class DataTransformationConfig:
    artifact_dir = os.path.join(artifact_folder)
    transformed_train_file_path = os.path.join(artifact_dir,'train.npy')
    transformed_test_file_path = os.path.join(artifact_dir,'test.npy')
    transformed_object_file_path = os.path.join(artifact_dir,'preprocessor.pkl')    #binary binary which will help for preprocessing(automation)

class DataTransformation:
    def __init__(self,feature_store_file_path):
        self.feature_store_file_path = feature_store_file_path  #our main data is stored inside this(mongodb data) which will be passed during creation of instance of class
        
        self.utils = MainUtils()
        self.data_transformation_config=DataTransformationConfig()

    @staticmethod
    def get_data(feature_store_file_path:str) -> pd.DataFrame:
        
        try:
            data = pd.read_csv(feature_store_file_path)

            data.rename(columns={"Good/Bad":TARGET_COLUMN},inplace=True)

            return data
        
        except Exception as e:
            raise CustomException(e,sys) from e
        
    def get_data_transformer_object(self):
        try:
            imputer_step = ('imputer',SimpleImputer(strategy='constant',fill_value=0))     #it will be used in replacing the null value with 0
            scaler_step = ('scaler',RobustScaler())

            preprocessor = Pipeline(steps=[imputer_step, scaler_step])

            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys) from e
        
    def initiate_data_transformation(self):
        
        logging.info("Entered initiate data transformation method of data transformation class")

        try:
            dataframe=self.get_data(feature_store_file_path=self.feature_store_file_path)   #consists the data

            X=dataframe.drop(columns=TARGET_COLUMN)
            y=np.where(dataframe[TARGET_COLUMN]==-1,0,1)    #if value is -1 then replace it with 0 else 1 as negative values are bit difficult to compute by machine

            X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)

            preprocessor = self.get_data_transformer_object() #Since preprocessor is a object

            X_train_scaled = preprocessor.fit_transform(X_train)
            X_test_scaled = preprocessor.transform(X_test)

            preprocessor_path = self.data_transformation_config.transformed_object_file_path    
            os.makedirs(os.path.dirname(preprocessor_path),exist_ok=True)

            self.utils.save_object(file_path=preprocessor_path,obj=preprocessor)

            train_arr = np.c_[X_train_scaled,np.array(y_train)]
            test_arr = np.c_[X_test_scaled,np.array(y_test)]

            return (train_arr,test_arr,preprocessor_path)
        
        except Exception as e:
            raise CustomException(e,sys) from e

