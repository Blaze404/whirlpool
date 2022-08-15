

def wrong_api_call_response(api):
    d = {
        "success": False,
        "message": "API call {} not supported".format(api)
    }
    return "API call {} not supported".format(api)
