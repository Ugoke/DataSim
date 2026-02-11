from datasim.generators.dataset import DatasetGenerator


class DataGenMeta(type):
    def __new__(mcls, name, bases, namespace):
        fields = {}

        for key, value in namespace.items():
            if not key.startswith("__") and not callable(value):
                fields[key] = value

        namespace["_fields"] = fields

        return super().__new__(mcls, name, bases, namespace)


class BaseDataGen(metaclass=DataGenMeta):
    __count__: int = 100
    __seed__: int = None
    __log__: bool = True

    @classmethod
    def generate(cls) -> DatasetGenerator:
        return DatasetGenerator(cls)
    
    @classmethod
    def generate_and_save(cls, path:str, file_type:str) -> DatasetGenerator:
        data = cls.generate()
        data.save(path, file_type)
        return data