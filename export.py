import os
import csv
import json
from datetime import datetime


class ExportBase:

    @classmethod
    def prepFile(cls, file, extension):
        if not file:
            now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file = 'C:/temp/rhyton/{}.{}'.format(now, extension.lower())

        directory = os.path.dirname(file)
        if not os.path.exists(directory):
            os.makedirs(directory)

        return file
    
class CSV(ExportBase):
    
    @classmethod
    def write(cls, data, file=None):
        file = cls.prepFile(file, 'csv')
        headers = set().union(*(d.keys() for d in data))

        with open(file, 'w', newline='') as f:
            writer = csv.DictWriter(
                    f,
                    fieldnames=headers.sort(),
                    extrasaction='ignore',
                    dialect='excel')
            writer.writeheader()
            writer.writerows(data)
        
        return file

    @staticmethod
    def append(data, file):
        try:
            with open(file, 'r', newline='') as f:
                reader = csv.reader(f, dialect='excel')
                headers = next(reader)
        except FileNotFoundError:
            print("File does not exist.")
        
        if headers:
            with open(file, 'a', newline='') as f:
                writer = csv.DictWriter(
                        f,
                        fieldnames=headers,
                        extrasaction='ignore',
                        dialect='excel')
                writer.writerows(data)

            return file


class JSON(ExportBase):
    
    @classmethod
    def write(cls, file, data):
        file = cls.prepFile(file, 'json')
        with open(file, 'w') as f:
            f.write(json.dumps(data))

        return file

    @staticmethod
    def append(file, data):
        try:
            with open(file, 'r') as f:
                existingData = json.loads(f)
        except FileNotFoundError:
            print("File does not exist.")
        
        if existingData:
            existingData + data
        else:
            existingData = data

        with open(file, 'w') as f:
            f.write(json.dumps(existingData))

        return file