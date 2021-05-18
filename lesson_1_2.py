import pytumblr
import json
from pprint import pprint

# https://www.programmableweb.com/category/all/apis
# https://www.tumblr.com/oauth/register
# https://api.tumblr.com/console/calls/user/info
# https://www.tumblr.com/docs/en/api/v2

# Authenticate via OAuth
client = pytumblr.TumblrRestClient(
  'hE7gmW3H3DuABcgE1HtIQ65STl***********************',
  'WEnHSp0jq9RhhvUnQi2ocmS9Bb***********************',
  'rJbuVYz6j4MTqfrmecDF5Tsan3***********************',
  'DxPj992Mp1ULM5XZQ5WpgmhBSt***********************'
)

# Make the request
#print(client.request.oauth)

# ampervadasz = client.posts('ampervadasz')
# print(json.dumps(ampervadasz['posts'], indent=4, sort_keys=True))
with open('tumblrAPI_test.json', 'w') as outfile:
    # json.dump(client.request.host, outfile)
    # json.dump(client.request.headers, outfile)
    json.dump(client.info(), outfile)