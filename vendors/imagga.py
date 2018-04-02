import requests
import json

def call_vision_api(image_filename, api_keys):
    api_key = api_keys['imagga']['api_key']
    api_secret = api_keys['imagga']['api_secret']

    # Via example found here:
    # https://github.com/cloudsight/cloudsight-python
    endpoint = "https://api.imagga.com/v1"



    response = requests.post(endpoint + '/content',auth=(api_key, api_secret), files={'image': open(image_filename, 'r')})
    response_dict = json.loads(response.text)
    for uploaded in response_dict['uploaded']:
        id = uploaded['id']
    response = requests.get(endpoint + '/tagging?content=' + id,
                        auth=(api_key, api_secret))
    response_dict = json.loads(response.text)
    return response_dict


def get_standardized_result(api_result):
    output = {
        'tags': [],
    }

    for tag_data in api_result['results'][0]['tags']:
        output['tags'].append((tag_data['tag'], tag_data['confidence']))

    return output
