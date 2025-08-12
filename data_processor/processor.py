from .loaders import DataLoader
from .exporters import DataExporter
from .combiner import DataCombiner

class DataProcessor:
    def __init__(self, loader: DataLoader, combiner_cls: type[DataCombiner], exporter: DataExporter):
        self.loader = loader
        self.combiner_cls = combiner_cls
        self.exporter = exporter

    def process(self, rooms_file: str, students_file: str, output_file: str) -> None:
        rooms = self.loader.load(rooms_file)
        students = self.loader.load(students_file)
        combiner = self.combiner_cls(rooms, students)
        combined_data = combiner.combine()
        self.exporter.export(combined_data, output_file)