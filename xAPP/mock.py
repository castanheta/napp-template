import requests


def example_get(invoker_url, target_url):
    # The invoker service will handle authentication
    full_target_url = target_url + "productOrder/get"
    response = requests.get(
        f"{invoker_url}/gateway/forward",
        params={"target_url": full_target_url}
    )
    return response

def example_wrong_post(invoker_url, target_url):
    full_target_url = target_url + "productOrder/post"
    body = {
        "id": "yetanother",  # str not allowed [,;="']
        "administrative_state": "UNLOCKED",  # LOCKED - UNLOCKED - SHUTTINGDOWN
        "operational_state": "ENABLED",  # ENABLED - DISABLED
        "coverage_area": ["IT"],  # ["IT"]
        "sst": 2,  # int 0 - 255
        "sd": "050505",  # str "6 numbers"
    }

    # The invoker service will handle authentication
    response = requests.post(
        f"{invoker_url}/gateway/forward",
        params={"target_url": full_target_url},
        json=body
    )
    return response


if __name__ == "__main__":

    invoker_url = "http://localhost:8008"
    target_url = "http://10.255.32.139:8000/api/slice-manager/v1/"

    
    response = example_get(invoker_url, target_url)
    # response = example_wrong_post(invoker_url, target_url)  # body is wrong

    # Check the response
    if response.status_code == 200 or response.status_code == 201:
        print("Success! Response:")
        print(response.text)
    else:
        print(f"Failed with status code {response.status_code}")
        print(response.text)