import requests
import json
import base64


def _convert_image_to_base64(image_filename):
    with open(image_filename, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string


def call_vision_api(image_filename, api_keys):
    api_key = api_keys['eyeem']

    headers = {'Authorization': api_key, 'Content-Type': 'application/json'}

    # Via example found here:
    # https://github.com/cloudsight/cloudsight-python
    endpoint = "https://vision-api.eyeem.com/v1"
    base64_image = _convert_image_to_base64(image_filename)

    post_payload = {
        "requests": [
            {
                "image": {
                    "content": base64_image
                },
                "tasks": [
                    {
                        "type": "TAGS"
                    }, {
                        "type": "CAPTIONS"
                    },
                    {
                        "type": "AESTHETIC_SCORE"
                    }
                ]
            }
        ]
    }

    response = requests.post(endpoint + '/analyze', headers=headers, json=post_payload)
    return response.json()


def get_standardized_result(api_result):
    output = {
        'tags': [],
        'captions': []
    }

    for captions in api_result['responses'][0]['captions']:
        output['captions'].append((captions['text'], float(1)))

    for tag_data in api_result['responses'][0]['tags']:
        output['tags'].append((tag_data['text'], tag_data['probability']))

    print output
    return output
