import pandas as pd


class CsvPipeline:
    def __init__(self, source_file):
        self.source_file = source_file
        self.source_data = None
        self.destination_data = None

    def extract(self):
        self.source_data = pd.read_csv(self.source_file)
        return self

    def transform(self):
        self.destination_data = self.source_data.to_dict(orient='records')
        return self

    def load(self):
        return self.destination_data
