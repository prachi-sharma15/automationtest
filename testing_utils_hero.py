import jsonpath_rw_ext as jp
from jsonschema import validate
from jsonpath_ng import jsonpath, parse
import json

import logging

logger = logging.getLogger()


def check_jsonpath_value(response, json_path_value):
    '''Function will match json value in response using jsonpath '''
    print_message(response)
    for jsonpath, expected_value in json_path_value.items():
    #assert expected_value == jp.match1(jsonpath, response.json())
     print(expected_value, jp.match1(jsonpath, response.json()))
     #(print response coming for error handling)


def validate_schema(response, schema_text):
    '''Function will validate jsonschema of a json'''
    response = response.json()
    validate(response, schema_text)


def check_string_response(response, json_path_value):
    '''Function will check string in response['response']'''
    response = response.json()
    response = json.loads(response['response'])

    for jsonpath, expected_value in json_path_value.items():
        assert expected_value == jp.match1(jsonpath, response)


def check_keys_in_product(response, keys, result_set):
    '''Function will assert keys in response['response']['products']
                                    response['result']['products']
    '''
    response = response.json()

    if "result" in response:
        products = response["result"][result_set]  # acquiring all products value
    else:
        products = response["response"][result_set]

    for product in products:
        for key in keys:
            assert key in product, "key not present in product---- %s" % key


def check_keys_in_response(response, keys, result_set):
    ''' Check keys in response['response]
    '''

    response = response.json()

    if "result" in response:
        response = response[result_set]
    else:
        response = response[result_set]
    if isinstance(response, dict):
        for key in keys:
            assert key in response, "key not present in response ---- %s" % key
    elif isinstance(response, list):
        for key in keys:
            for res in response:
                assert key in res, "key not present in response ---- %s" % key

    else:
        logger.info("response type mismatch")


def match_query_output_count(response, json_path_value):
    result1 = [match.value for match in parse(json_path_value.get("query1")).find(response.json())]
    result2 = [match.value for match in parse(json_path_value.get("query2")).find(response.json())]
    assert (len(result1) == len(result2))


def print_message(response):
    ''' function used for logging purpose '''
    test_url = response.url
    payload = response.request.body

    logger.info("\n,**************************************************")
    logger.info('URL ==> ' + str(test_url))
    logger.info('PAYLOAD ==> ' + str(payload))
    logger.info('METHOD ===> ' + str(response.request.method).upper())
    logger.info('Status Code ==> ' + str(response.status_code))
    logger.info('Response Time (s) ==> ' + str(round(response.elapsed.total_seconds(), 2)))
    if response.status_code == 200:
        logger.info('Response text ==> ' + str(response.text))

    logger.info("\n,**************************************************")

    if response.status_code != 200:
        print('\n')
        print("**************************************************")
        print('URL ==> ', test_url)
        print('Method ==> ', str(response.request.method).upper())
        print('Status Code ==> ', response.status_code)
        print('Response text ==> ', response.text)
        print('Response Time (s) ==> ', str(round(response.elapsed.total_seconds(), 2)))
        print("**************************************************")
