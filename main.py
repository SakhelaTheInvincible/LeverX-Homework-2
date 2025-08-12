from data_processor.loaders import JsonDataLoader
from data_processor.exporters import get_exporter
from data_processor.combiner import DataCombiner
from data_processor.processor import DataProcessor
import argparse
import os

def parse_args():
    parser = argparse.ArgumentParser(description="Combine rooms and students data.")
    parser.add_argument("--students", required=True, help="Path to students JSON file")
    parser.add_argument("--rooms", required=True, help="Path to rooms JSON file")
    parser.add_argument("--output-format", required=True, choices=["json", "xml"], help="Output format")
    parser.add_argument("--output-name", required=True, help="Output file name (without extension)")
    return parser.parse_args()


def main():
    # example call:
    # python main.py --students input/students.json --rooms input/rooms.json --output-format json --output-name test
    
    args = parse_args()
    os.makedirs("output", exist_ok=True)
    output_file = f"output/{args.output_name}.{args.output_format}"

    loader = JsonDataLoader()
    exporter = get_exporter(args.output_format)

    processor = DataProcessor(loader, DataCombiner, exporter)
    processor.process(args.rooms, args.students, output_file)

    print(f"Data saved to {output_file}")

if __name__ == '__main__':
    main()