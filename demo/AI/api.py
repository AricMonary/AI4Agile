import requests
from requests.auth import HTTPBasicAuth
import json

url = "https://playingabout.atlassian.net/rest/api/3/issue"

auth = HTTPBasicAuth("aric.monary@wsu.edu", "NCx7f7ZWle5yfwS3DB8JBCEA")

headers = {
   "Accept": "application/json",
   "Content-Type": "application/json"
}

payload = json.dumps( {
  "update": {},
  "fields": {
    "summary": "Main order flow broken",
    "parent": {
      "key": "AI4-107"
    },
    "issuetype": {
      "id": "10004"
    },
    "project": {
      "id": "10000"
    },
    "description": "yes"
  }
} )

response = requests.request(
   "POST",
   url,
   data=payload,
   headers=headers,
   auth=auth
)

print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))