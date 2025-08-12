import json
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import xml.etree.ElementTree as ET
from xml.dom import minidom

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


EXPORTERS = {
    "json": JsonExporter,
    "xml": XmlExporter,
}

def get_exporter(format_name):
    try:
        return EXPORTERS[format_name.lower()]()
    except KeyError:
        raise ValueError(f"Unsupported export format: {format_name}")