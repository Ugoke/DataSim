

class DataGenMeta(type):
    def __new__(mcls, name, bases, namespace):
        fields = {
            k: v for k, v in namespace.get("__annotations__", {}).items()
        }
        namespace["_fields"] = fields
        return super().__new__(mcls, name, bases, namespace)


class BaseDataGen(metaclass=DataGenMeta):
    __count__ = 100
    __file_type__ = "csv"
    __seed__: int = None
    __log__ = True

    @classmethod
    def generate(cls, path):
        from datasim.generators.dataset import DatasetGenerator
        gen = DatasetGenerator(cls)
        gen.write(path)