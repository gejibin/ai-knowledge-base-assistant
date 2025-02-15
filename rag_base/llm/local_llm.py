
import sys
import os              

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())


class LocalModels():
    def __init__(self):
        self.local_model_url = ""
        self.local_model_enable = False
        self.local_model_default = "llama3:latest"
        self.llm_model_list = []
        self.local_model_enable = os.environ.get("LOCAL_MODEL_ENABLE")
        if self.local_model_enable:
            models = os.environ.get("LOCAL_MODELS")
            self.local_model_url = os.environ.get("LOCAL_MODEL_URL")
            self.local_model_default = os.environ.get("LOCAL_MODEL_DEFAULT")
            self.llm_model_list = models.split(",")
            #print(self.llm_model_list)




    def get_local_models(self):
        return self.llm_model_list
