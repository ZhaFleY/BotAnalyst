import pyreadstat
from aiogram.fsm.state import StatesGroup
import pandas as pd
import requests
from utils.logger import logger
import pyreadstat as ps
class FileProcessor:
    def __init__(self, document):
        self.document = document

    def process(self):

        document = self.document
        format = document.split(".")[-1]
        print(f"format - {format}")



        match format:

            case "csv":
                dataset = pd.read_csv(document)
                flag = "csv"
                return dataset,None,flag
            case "xlsx":
                dataset = pd.read_excel(document)
                flag = "xlsx"
                return dataset,None,flag
            case "sav":
                dataset,meta = pyreadstat.read_sav(document)
                flag = "sav"
                return dataset,meta,flag
















