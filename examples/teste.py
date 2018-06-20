import base64
import json

with open('obama_small.jpg','rb') as f:
    foto = f.read()
sensor_data = {}
sensor_data['t'] = 1
sensor_data['h'] = 2
sensor_data['img'] = base64.b64encode(foto)
json_data = json.dumps(sensor_data)

print(json_data)
