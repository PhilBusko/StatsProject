"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
CRIME DATA HELPER
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import requests
from requests.exceptions import HTTPError
import time
import math


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
CONSTANTS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

BASE_URL = 'https://api.usa.gov/crime/fbi/sapi/'
API_KEY = 'nRdG8cJGUQdri4Ki1skMMeI1J4aZD0K8fvxcxC5X' 

# dict or list of agencies, provides agency ORI
LOOKUP_AGENCIES = '/api/agencies'                                        
LOOKUP_AGENCIES_LIST = '/api/agencies/list'
LOOKUP_AGENCIES_STATE = '/api/agencies/byStateAbbr/raw/{stateAbbr}'     

# region property of agency
LOOKUP_REGIONS = '/api/regions'
LOOKUP_REGION_PROPS = '/api/regions/{regionName}'

# state property of agency
LOOKUP_STATES = '/api/states'
LOOKUP_STATE_PROPS = '/api/states/{stateAbbr}'

# summary per agency
SUMMARY_AGENCY = '/api/summarized/agencies/{ori}/offenses/{since}/{until}'
SUMMARY_AGENCY_OFFENSE = '/api/summarized/agencies/{ori}/{offense}/{since}/{until}'
SUMMARY_STATE_OFFENSE = '/api/summarized/state/{stateAbbr}/{offense}/{since}/{until}'

# offense-tkm
OFFENSE_AGENCY = '/api/nibrs/{offense}/offense/agencies/{ori}/{variable}'
OFFENSE_NATIONAL = '/api/nibrs/{offense}/offense/national/{variable}'
OFFENSE_REGION = '/api/nibrs/{offense}/offense/regions/{regionName}/{variable}'
OFFENSE_STATE = '/api/nibrs/{offense}/offense/states/{stateAbbr}/{variable}'



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
FUNCTIONS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


# get an endpoint that is NOT paginated
def get_json(endpoint, endpoint_config={}, add_params={}, paginated=False):

    endpoint_url = f'{BASE_URL}{endpoint}'

    for key, val in endpoint_config.items():
        endpoint_url = endpoint_url.replace(key, val)

    params = {
        'api_key': API_KEY
    }
    params.update(add_params)

    #print(params)

    try:
        response = requests.get(endpoint_url, params=params)
    except Exception as ex:
        print(f'{endpoint_url} | {params})')
        raise ex

    # if the endpoint is not paginated return the current result

    if not paginated:
        return response.json()

    # if the endpoint is paginated, aggregate the results 

    else:
        return get_paginated(endpoint_url, response)


def get_paginated(endpoint_url, paginated_response)

    # a paginated response has a wrapper dict for pagination info
    # response = {'results': [...], 'pagination': [...] }

    pagination = paginated_response.json().get('pagination')
    print(pagination)
    max_pages = math.ceil( pagination.get('count') / pagination.get('per_page') )
    response_ls = []

    for page_no in range(max_pages):

        params['page'] = page_no

        try:
            response = requests.get(endpoint_url, params=params)
            time.sleep(.1)
        except Exception as ex:
            print(f'{endpoint_url} | {params})')
            raise ex

        results = response.json().get('results')
        print(f'page {page_no}: len {len(results)}')
 
        response_ls += results

    return response_ls

