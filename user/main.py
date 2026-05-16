from quality_checks import api_response_is_not_null
from api_caller import call_ollama

test_case = {
"prompt" : "why is sky blue? Tell me in one line",
"tags": ["Sky", "Blue", "Scattering"] 
}



def run_quality_check(test_case):
    response = call_ollama(test_case["prompt"]).json()["response"]
    # print(response)
    api_response_is_not_null(response)
    tags_lower = []
    resposne_l = response.lower()
    for tag in test_case["tags"]:
        tags_l = tag.lower()
        tags_lower.append(tags_l)

    if any(tag in resposne_l for tag in tags_lower):
        print("tags match")
        print(resposne_l)
        print(tags_lower)
    else:
        print("tags did not match")
        print(resposne_l)
        print(tags_lower)


# def check_api_response_is_not_null(response):
#     api_response_is_not_null(response)



run_quality_check(test_case)




