

def api_response_is_not_null(response):
    cleaned_response = response.strip()
    if len(cleaned_response)>0:
        print("we have valid response")
    else:
        print("We have invalid reposne")

    return {
        "check":"response not empty",
        "reason": "Response has content"
    }
        


