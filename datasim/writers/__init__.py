from .csv import CSVWriter
from .json import JSONWriter


def get_writer(file_type):
    if file_type == "csv":
        return CSVWriter()
    elif file_type == "json":
        return JSONWriter()
    else:
        raise ValueError(f"Unsupported file format: {file_type}")