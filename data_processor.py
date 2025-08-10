import json
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os

class DataLoader(ABC):
    @abstractmethod
    def load(self, file_path: str) -> List[Dict[str, Any]]:
        pass

class JsonDataLoader(DataLoader):
    def load(self, file_path: str) -> List[Dict[str, Any]]:
        with open(file_path, 'r') as file:
            return json.load(file)

class DataCombiner:
    def __init__(self, rooms: List[Dict[str, Any]], students: List[Dict[str, Any]]):
        self.rooms = rooms
        self.students = students

    def combine(self) -> List[Dict[str, Any]]:
        room_dict = {room['id']: {'id': room['id'], 'name': room['name'], 'students': []} 
                    for room in self.rooms}
        
        for student in self.students:
            room_id = student['room']
            if room_id in room_dict:
                room_dict[room_id]['students'].append({
                    'id': student['id'],
                    'name': student['name']
                })
        
        return list(room_dict.values())

class DataExporter(ABC):
    @abstractmethod
    def export(self, data: List[Dict[str, Any]], output_file: str) -> None:
        pass

class JsonExporter(DataExporter):
    def export(self, data: List[Dict[str, Any]], output_file: str) -> None:
        with open(output_file, 'w') as file:
            json.dump(data, file, indent=2)

class XmlExporter(DataExporter):
    def export(self, data: List[Dict[str, Any]], output_file: str) -> None:
        root = ET.Element('rooms')
        
        for room in data:
            room_element = ET.SubElement(root, 'room', id=str(room['id']))
            name_element = ET.SubElement(room_element, 'name')
            name_element.text = room['name']
            
            students_element = ET.SubElement(room_element, 'students')
            for student in room['students']:
                student_element = ET.SubElement(students_element, 'student', id=str(student['id']))
                student_element.text = student['name']
        
        xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
        with open(output_file, 'w') as file:
            file.write(xml_str)

class DataProcessor:
    def __init__(self, loader: DataLoader, combiner: DataCombiner, exporter: DataExporter):
        self.loader = loader
        self.combiner = combiner
        self.exporter = exporter

    def process(self, rooms_file: str, students_file: str, output_file: str) -> None:
        self.loader.load(rooms_file)
        self.loader.load(students_file)
        combined_data = self.combiner.combine()
        self.exporter.export(combined_data, output_file)

def get_user_input(prompt: str, validation_func=None) -> str:
    user_input = input(prompt).strip()
    if not validation_func or validation_func(user_input):
        return user_input
    print("Invalid input. Please try again.")

def validate_file_exists(file_path: str) -> bool:
    try:
        with open(file_path, 'r'):
            return True
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return False

def validate_output_format(format_str: str) -> bool:
    return format_str.lower() in ['json', 'xml']

def main():
    print("Please provide the following information:")
    
    # input
    students_file = get_user_input(
        "Path to students JSON file: ",
        validate_file_exists
    )
    
    rooms_file = get_user_input(
        "Path to rooms JSON file: ",
        validate_file_exists
    )
    
    # output
    output_format = get_user_input(
        "Output format (json/xml): ",
        validate_output_format
    ).lower()
    
    output_base = get_user_input(
        "Output file name (without extension): ",
        lambda x: bool(x.strip())
    )
    
    # output must be saved in output directory
    os.makedirs("output", exist_ok=True)
    output_file = f"output/{output_base}.{output_format}"
    
    # process
    loader = JsonDataLoader()
    rooms = loader.load(rooms_file)
    students = loader.load(students_file)
    combiner = DataCombiner(rooms, students)
    
    if output_format == 'json':
        exporter = JsonExporter()
    else:
        exporter = XmlExporter()
    
    processor = DataProcessor(loader, combiner, exporter)
    processor.process(rooms_file, students_file, output_file)
    
    print(f"Data successfully processed")

if __name__ == '__main__':
    main()