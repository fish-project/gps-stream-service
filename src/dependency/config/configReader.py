import json
from pathlib import Path

'''
data: dữ liệu config lấy từ <resources/config.json>
'''

json_file_path = Path('resources/config.json')

with open(json_file_path, 'r') as file:
    data = json.load(file)