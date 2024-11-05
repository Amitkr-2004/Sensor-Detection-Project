import os
import sys
import pandas as pd
import pickle
from flask import request
from src.logger import logging
from src.constant import *
from src.exception import CustomException
from src.utils.main_utils import MainUtils
from dataclasses import dataclass

@dataclass
class PredictPipelineConfiguration:     #here output will be stored
    predict_output_dirname:str = "predictions"
    predict_filename:str = "prediction_file.csv"
    model_file_path:str = os.path.join(artifact_folder,"model.pkl")  #at this path the best model is stored
    preprocessor_path:str = os.path.join(artifact_folder,"preprocessor.pkl")    #at this path best preprocessor details are stored 
    predict_file_path:str = os.path.join(predict_output_dirname,predict_filename)

class PredictPipeline:
    def __init__(self,request=request):
        self.request=request
        self.utils=MainUtils()
        self.predict_pipeline_config = PredictPipelineConfiguration()

    def save_input_files(self)->str:        #here input database will be stored
        try:
            predict_file_input_dir = "prediction_artifacts"
            os.makedirs(predict_file_input_dir,exist_ok=True)

            input_csv_file=self.request.files['file']
            pred_file_path = os.path.join(predict_file_input_dir,input_csv_file.filename)

            input_csv_file.save(pred_file_path)

            return pred_file_path
        except Exception as e:
            raise CustomException(e,sys) from e

    def predict(self,features):
        try:
            model=self.utils.load_object(file_path=self.predict_pipeline_config.model_file_path)         
            preprocessor=self.utils.load_object(file_path=self.predict_pipeline_config.preprocessor_path)

            transform_x = preprocessor.transform(features)
            preds = model.predict(transform_x)

            return preds
        except Exception as e:
            raise CustomException(e,sys) from e
    
    def get_predicted_output(self,input_dataFrame_path: pd.dataFrame):
        try:
            prediction_column_name:str = TARGET_COLUMN

            input_dataFrame:pd.DataFrame = pd.read_csv(input_dataFrame_path)

            input_dataFrame = input_dataFrame.drop(columns = "Unnamed: 0") if "Unnamed: 0" in input_dataFrame else input_dataFrame

            predictions=self.predict(input_dataFrame)

            input_dataFrame[prediction_column_name] = [pred for pred in predictions]

            target_column_mapping = {0:"Bad",1:"Good"}

            input_dataFrame[prediction_column_name] = input_dataFrame[prediction_column_name].map(target_column_mapping)

            os.makedirs(self.predict_pipeline_config.predict_output_dirname,exist_ok=True)

            input_dataFrame.to_csv(self.predict_pipeline_config.predict_file_path,index=False)

            logging.info("Predictions Completed")

        except Exception as e:
            raise CustomException(e,sys) from e
        
    def run_pipeline(self):
        try:
            input_file_path=self.save_input_files()

            self.get_predicted_output(input_dataFrame_path=input_file_path)

            return self.predict_pipeline_config

        except Exception as e:
            raise CustomException(e,sys) from e
