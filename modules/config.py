import json

def get_config():
    with open('config.json') as json_file:
        data = json.load(json_file)
    return data

def check_config():
    try:
        with open('config.json') as json_file:
            data = json.load(json_file)
        return True
    except:
        return False