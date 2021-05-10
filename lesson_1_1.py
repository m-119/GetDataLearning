import json
import requests
import os
from pprint import pprint
# вариант с авторизацией
# username = 'm-119'
# token = os.environ.get("d2e75fa1a36d189eff33d981f***************")
# r = requests.get(f"https://api.github.com/users/{username}/repos", auth=(username, token))
# pprint(r.text)

# вариант без авторизации
username = "m-119"
url = f"https://api.github.com/users/{username}/repos"
user_data = requests.get(url).json()
with open('gitAPI_test.json', 'w') as outfile:
    # json.dump(client.request.host, outfile)
    # json.dump(client.request.headers, outfile)
    json.dump(user_data, outfile, indent=4)