from aiogram.fsm.state import StatesGroup
import pandas as pd
import requests
from utils.logger import logger
import pyreadstat as ps
class FileProcessor:
    def __init__(self, document):
        self.document = document

    def process(self):

        dataset = None
        meta = None
        flag = None

        try:
            dataset = pd.read_csv(self.document)
            flag = "csv"
            return dataset, meta, flag
        except:
            pass
        try:
            dataset = pd.read_excel(self.document)
            flag = "excel"
            return dataset, meta, flag

        except: pass

        try:
            dataset,meta = ps.read_sav(self.document)
            flag = "sav"
            return dataset,meta,flag
        except:
            pass

        finally:
            print('ERROR')
            pass







