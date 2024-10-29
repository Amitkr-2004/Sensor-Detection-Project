import sys
import os
import pandas as pd
import numpy as np
from pymongo import MongoClient
from zipfile import Path

from src.constant import *
from src.utils.main_utils import MainUtils
from src.logger import logging
from src.exception import CustomException
from dataclasses import dataclass   #By using dataclasses we need not to introduce constructor of class, it is used to initialize value

@dataclass
class DataIngestionConfig:      #this class is defined for creation of artifact folder in our local system to store the mongodb data
    artifact_folder:str = os.path.join(artifact_folder)     #dataclass is used to define it thus __int__ is not used

class DataIngestion:
    def __init__(self):
        self.data_ingestion_config=DataIngestionConfig()
        self.util=MainUtils()

    def export_collection_as_dataframe(self,collection_name,db_name):

        try:
            client=MongoClient(MONGO_DB_URL)
            collection=client[db_name][collection_name]
            df =pd.DataFrame(list(collection.find()))

            if '_id' in df.columns.to_list:
                df=df.drop(columns=['_id'],axis=1)
            
            df.replace({'na':np.nan},inplace=True)

            return df
        
        except Exception as e:
            raise CustomException(e,sys) from e
        
    def export_data_into_feature_store_file_path(self):
        try:
            logging.info(f'Exporting Data from mongodb')

            raw_file_path=self.data_ingestion_config.artifact_folder

            os.makedirs(raw_file_path,exist_ok=True)

            sensor_data = self.export_collection_as_dataframe(      # all data of mongodb is stored here
                collection_name=MONGO_COLLECTION_NAME,
                db_name=MONGO_DATABASE_NAME
            )

            logging.info(f"saving exported data into feature store file path : {raw_file_path}")

            feature_store_file_path = os.path.join(raw_file_path,'wafer.csv')

            sensor_data.to_csv(feature_store_file_path,index=False)

            return feature_store_file_path      #it finally returns the file_path
        
        except Exception as e:
            raise CustomException(e,sys) from e 
        
    def initiate_data_ingestion(self):  #By calling this method automatically both above methods are called as they are interconnected and as we can see that 1st method return dataFrame and second method returns filepath therefore both we will get
        logging.info("Entered initiated_data_ingestion method of data_integration class")

        try:
            feature_Store_file_path=self.export_data_into_feature_store_file_path()

            logging.info("got the data from mongodb")

            logging.info("exited initiate_data_ingestion method of data ingestion class")
            
            return feature_Store_file_path
        except Exception as e:
            raise CustomException(e,sys) from e

        

        
    

    

