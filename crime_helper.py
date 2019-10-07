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

BASE_URL = 'https://api.usa.gov/crime/fbi/sapi'
API_KEY = 'nRdG8cJGUQdri4Ki1skMMeI1J4aZD0K8fvxcxC5X' 

LOOKUP_AGENCIES = '/api/agencies'                                        
LOOKUP_AGENCIES_LIST = '/api/agencies/list'
LOOKUP_AGENCIES_STATE = '/api/agencies/byStateAbbr/raw/{stateAbbr}'     
LOOKUP_REGIONS = '/api/regions'
LOOKUP_REGION_PROPS = '/api/regions/{regionName}'
LOOKUP_STATES = '/api/states'
LOOKUP_STATE_PROPS = '/api/states/{stateAbbr}'

SUMMARY_AGENCY = '/api/summarized/agencies/{ori}/offenses/{since}/{until}'
SUMMARY_AGENCY_OFFENSE = '/api/summarized/agencies/{ori}/{offense}/{since}/{until}'
SUMMARY_STATE_OFFENSE = '/api/summarized/state/{stateAbbr}/{offense}/{since}/{until}'

OFFENSE_AGENCY = '/api/nibrs/{offense}/offense/agencies/{ori}/count'
OFFENSE_NATIONAL = '/api/nibrs/{offense}/offense/national/count'
OFFENSE_REGION = '/api/nibrs/{offense}/offense/regions/{regionName}/count'
OFFENSE_STATE = '/api/nibrs/{offense}/offense/states/{stateAbbr}/count'

EMPLOYMENT_AGENCY = '/api/police-employment/agencies/{ori}/{since}/{until}'
EMPLOYMENT_YEAR = '/api/police-employment/dl/agency/{year}'
EMPLOYMENT_NATIONAL =  '/api/police-employment/national/{since}/{until}'
EMPLOYMENT_REGION = '/api/police-employment/regions/{regionName}/{since}/{until}'
EMPLOYMENT_STATE = '/api/police-employment/states/{stateAbbr}/{since}/{until}'

VICTIM_AGENCY = '/api/data/nibrs/{offense}/victim/agencies/{ori}/{variable}'
VICTIM_NATIONAL = '/api/data/nibrs/{offense}/victim/national/{variable}'
VICTIM_REGION = '/api/data/nibrs/{offense}/victim/regions/{regionName}/{variable}'
VICTIM_STATE = '/api/data/nibrs/{offense}/victim/states/{stateAbbr}/{variable}'

OFFENDER_AGENCY = '/api/data/nibrs/{offense}/offender/agencies/{ori}/{variable}'
OFFENDER_NATIONAL = '/api/data/nibrs/{offense}/offender/national/{variable}'
OFFENDER_REGION = '/api/data/nibrs/{offense}/offender/regions/{regionName}/{variable}'
OFFENDER_STATE = '/api/data/nibrs/{offense}/offender/states/{stateAbbr}/{variable}'


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
FUNCTIONS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


# entry point for getting data from api
def get_json(endpoint, endpoint_config={}, add_params={}):

    endpoint_url = f'{BASE_URL}{endpoint}'

    for key, val in endpoint_config.items():
        endpoint_url = endpoint_url.replace(key, val)

    #print(endpoint_url)

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

    response_json = response.json()

    # if the endpoint is not paginated return the current result

    if 'pagination' not in response_json:
        return response_json

    # if the endpoint is paginated, aggregate the results 
    # response = {'results': [...], 'pagination': [...] }

    else:
        pagination = response_json.get('pagination')
        print(pagination)
        return get_paginated(endpoint_url, params, pagination)


# called by get_json when endpoint type is paginated
def get_paginated(endpoint_url, params, pagination):

    max_pages = pagination.get('pages')
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

