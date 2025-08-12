def validate_file_exists(file_path: str) -> bool:
    try:
        with open(file_path, 'r'):
            return True
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return False

def validate_output_format(format_str: str) -> bool:
    return format_str.lower() in ['json', 'xml']