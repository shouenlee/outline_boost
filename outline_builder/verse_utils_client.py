import requests

class VerseUtilsClient:
    @staticmethod
    def post_request(url, reference, headers=None):
        data = {
            'reference': reference
        }
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

        response = requests.post(url, json=data, headers=headers)
        #print(response.content)
        #print(response.text)
        #print(response.reason)
        
        try:
            response_json = response.json()
            if response.status_code != 200:
                print(f"verse_requestor error: {response_json.get('error')}")
                print(f"query: {data}")
                return None
        except requests.exceptions.JSONDecodeError:
            return None
        
        return response_json.get("output")