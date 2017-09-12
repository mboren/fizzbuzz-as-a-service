# -*- coding: utf-8 -*-

import fizzbuzz as fb
import json


def parse_int_quietly(s):
    try:
        result = int(s)
    except ValueError:
        result = None

    return result


def make_response(err, res=None):
    if err:
        body = { 'error': err }
        status_code = '400'
    else:
        body = res
        status_code = '200'

    return {
        'statusCode': status_code,
        'body': json.dumps(body),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Credentials': True
        },
    }


def handler(event, context):
    operation = event['httpMethod']

    if operation == 'GET':
        query_parameters = event['queryStringParameters']

        if (query_parameters is not None) and 'data' in query_parameters:
            data = query_parameters['data']
            parsed_data = (parse_int_quietly(i) for i in data.split(','))
            filtered_data = (i for i in parsed_data if i is not None)
            result = [{"in": i, "out": fb.fizzbuzz(i)} for i in filtered_data]

            return make_response(None, result)
        else:
            return make_response('missing query param: data')
    else:
        return make_response('only GET is supported')
