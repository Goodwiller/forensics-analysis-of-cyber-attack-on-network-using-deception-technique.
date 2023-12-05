import re
import json

def extract_ip_and_port(line):
    pattern = r'(\d+\.\d+\.\d+\.\d+):(\d+)'
    match = re.search(pattern, line)

    if match:
        ip_address = match.group(1)
        port = match.group(2)
        return ip_address, port

    return None, None

def parse_log(log_file_path, output_json_file):
    with open(log_file_path, 'r', encoding='utf-8') as file:
        log_lines = file.readlines()

    json_objects = []

    for line in log_lines:
        # Check for disconnect event
        if 'honeytrap/server ▶ DEBU' in line and 'Disconnected connection' in line:
            first_ip, second_ip = extract_ip_and_port(line)
            print("Connection from %s:%s disconnected" % (first_ip, second_ip))

        # Extract JSON payload
        try:
            json_data = json.loads(line)
            print("JSON Payload:", json_data)
            json_objects.append(json_data)
        except json.JSONDecodeError:
            pass

    # Write JSON objects to a file with newline delimiter
    with open(output_json_file, 'w', encoding='utf-8') as json_file:
        for obj in json_objects:
            json_file.write(json.dumps(obj))
            json_file.write('\n')

if __name__ == "__main__":
    log_file_path = '/content/honeytrap.txt'  # Replace with your actual log file path
    output_json_file = '/content/output.json'  # Replace with your desired output JSON file path
    parse_log(log_file_path, output_json_file)