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
    return {
        'statusCode': '400' if err else '200',
        'body': json.dumps(err) if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def handler(event, context):
    operation = event['httpMethod']

    if operation == 'GET':
        query_parameters = event['queryStringParameters']

        if (query_parameters is not None) and 'data' in query_parameters:
            data = query_parameters['data']
            parsed_data = parse_int_quietly(data)

            if parsed_data is not None:
                result = fb.fizzbuzz(parsed_data)
                return make_response(None, result)
            else:
                return make_response('failed to convert "{}" to int'.format(data))
        else:
            return make_response('missing query param: data')
    else:
        return make_response('only GET is supported')
