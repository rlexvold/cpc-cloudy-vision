from eightbit.client import EightbitApi
import time

def call_vision_api(image_filename, api_keys):
    api_key = api_keys['8bit']

    api = EightbitApi(apikey=api_key)
    results = api.tag_file(image_filename, modelkey='object')
    print(results)
    time.sleep(5)
    return results.json()


def get_standardized_result(api_result):
    output = {
        'tags': [],
    }

    for tag_data in api_result['results'][0]['tags']:
        output['tags'].append((tag_data['tag'], tag_data['confidence']))

    return output
