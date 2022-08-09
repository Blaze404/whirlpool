def unsupported_request_type(t):
    return {'success': False,
            "message": "Request type {} not supported. Send POST request".format(t),
            "data": None,
            "log": "None"
            }
