"""JSON helper functions"""
import json

from django.http import HttpResponse


def json_response(data=None, message=None, status=200):
    resp = dict()
    if message:
        resp['message'] = message
    if data:
        resp.update(data)
    return HttpResponse(json.dumps(resp, sort_keys=True),
                        content_type='application/json'
                        )


def json_error(error_string, status=400):
    data = {
        'errors': error_string,
    }
    return HttpResponse(json.dumps(data, sort_keys=True), status=status,
                        content_type='application/json')
