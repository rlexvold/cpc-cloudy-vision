import base64
import json
import requests
from threadgenius.client import ThreadGenius
from threadgenius.types import ImageFileInput

def call_vision_api(image_filename, api_keys):
    api_key = api_keys['threadgenius']
    tg = ThreadGenius(api_key=api_key)

    with open(image_filename, 'rb') as image_file:
        image = ImageFileInput(file_object=image_file)
        result = tg.tag_image(image=image)

    return result


# See this function in microsoft.py for docs.
def get_standardized_result(api_result):
    output = {
        'tags' : [],
    }

    try:
        for tags in api_result['response']['prediction']['data']['tags']:
            output['tags'].append((tags['name'], tags['confidence']))
    except:
        print 'error with output'
        print api_result

    return output
