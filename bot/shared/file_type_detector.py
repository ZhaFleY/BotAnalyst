import pandas as pd
import pyreadstat


class FileDetection:
    def __init__(self, document: str):
        self.document = document

    def process(self):
        document = self.document
        file_format = document.split(".")[-1].lower()

        match file_format:
            case "csv":
                dataset = pd.read_csv(document)
                return dataset, None, "csv"
            case "xlsx":
                dataset = pd.read_excel(document)
                return dataset, None, "xlsx"
            case "sav":
                dataset, meta = pyreadstat.read_sav(document)
                return dataset, meta, "sav"
            case _:
                return None, None, "unknown"

