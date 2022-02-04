import requests
import json
import time

device_id = ''
with open('./DEVICEID', 'r') as f:
    device_id = f.read()
assert len(device_id) == 128

def dock(base_url='http://localhost:3456'):
    url = base_url + '/v1/iot/device/dock'
    r = requests.post(url, json={'device_id': device_id}, stream=True)
    if r.status_code != 200:
        print('Error:', r.status_code, r.json()['msg'])
        return False
    for chunk in r.raw.read_chunked():
        data = json.loads(chunk.decode('utf-8'))
        if data['type'] == 'heartbeat':
            send_heartbeat(base_url, data['id'])
            continue
        elif data['type'] == 'greeting':
            continue
        yield data
        
def send_heartbeat(base_url: str, id_: str):
    requests.post(
        base_url + '/v1/iot/device/heartbeat',
        json={
                'device_id': device_id,
                'time': int(time.time()),
                'uuid': id_
            }
    )