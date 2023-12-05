import json


def convert_to_json_array(input_file, output_file):
    try:
        # Read and parse each line
        with open(input_file, 'r') as file:
            json_objects = [json.loads(line) for line in file]

        # Write the list as a JSON array
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(json_objects, file, ensure_ascii=False, indent=4)

        print(f"File converted successfully. Output: {output_file}")

    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
input_file = 'Manhattan.json'  # Replace with your input file name
output_file = 'output Manhattan.json'         # Replace with your desired output file name

convert_to_json_array(input_file, output_file)
