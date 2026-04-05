from utils.file_processor import FileProcessor

import requests
import json


def send_to_agent(path):

    processor = FileProcessor(path)
    data, meta,flag = processor.process()

    print(data, meta, flag)



