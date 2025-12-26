from .csv import CSVWriter
from .json import JSONWriter
from .base import Writer


def get_writer(file_type):
    if isinstance(file_type, type) and issubclass(file_type, Writer):
        return file_type()
    
    writer_classes = {
        "csv": CSVWriter,
        "json": JSONWriter
    }
    
    if file_type in writer_classes:
        return writer_classes[file_type]()
    
    raise ValueError(f"Unsupported file format: {file_type}")