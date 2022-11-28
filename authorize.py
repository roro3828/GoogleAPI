import json
import requests
import time

import googleapi

with open("client.json","r",encoding="utf-8") as f:
    data=json.load(f)

scopes="https://www.googleapis.com/auth/youtube"

g=googleapi.GoogleAPI(data["web"]["client_id"],client_secret=data["web"]["client_secret"],app_name=data["web"]["project_id"],scopes=scopes)

print(g.generate_authorization_url())
c=input()
print(g.access_token_request(c).text)
g.save_keys()