from flask import Flask,request,render_template,send_file
from src.exception import CustomException
from src.logger import logging
import os,sys

from src.pipeline.predict_pipeline import PredictPipeline
from src.pipeline.train_pipeline import TrainingPipeline

app=Flask(__name__)

@app.route("/")
def home():
    return "Welcome to my Website"

@app.route("/train")
def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()

        return "Training Completed"

    except Exception as e:
        raise CustomException(e,sys) from e
    
@app.route("/predict",methods=['POST','GET'])
def upload():
    try:

        if(request.method=='POST'):
            prediction_pipeline = PredictPipeline(request)
            
            prediction_pipeline_detail = prediction_pipeline.run_pipeline()  #through request whole file is sent

            logging.info("prediction completed. Downloading prediction file.")

            return send_file(prediction_pipeline_detail.predict_file_path,
                             download_name=prediction_pipeline_detail.predict_filename,
                             as_attachment=True)
        
        else:
            return render_template('upload_file.html')  #for Get request just return the html page
    
    except Exception as e:
        raise CustomException(e,sys) from e


if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
