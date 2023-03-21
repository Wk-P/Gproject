import json

#将输出存储在 output_data 变量中
with open('output_data.json', 'w') as f:
    json.dump(output_data, f)