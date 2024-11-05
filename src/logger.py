import logging
import os
from datetime import datetime
import time

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M')}_{int(time.time())}.log"#format of the file that will be stored in the log file

logs_path=os.path.join(os.getcwd(),"logs",LOG_FILE)     #current Directory/logs/LOG_FILE format

os.makedirs(logs_path,exist_ok=True)    #it helps in making the directories

LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO 
)

