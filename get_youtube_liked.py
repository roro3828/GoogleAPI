import json
import requests
import time

import googleapi

"""with open("client_secrets.json","r",encoding="utf-8") as f:
    data=json.load(f)

g=googleapi.GoogleAPI(data["web"]["client_id"],client_secret=data["web"]["client_secret"],scopes="https://www.googleapis.com/auth/youtube")

print(g.generate_authorization_url())
c=input()
print(g.access_token_request(c).text)
g.save_keys()"""

g=googleapi.GoogleAPI()
g.read_keys()

if g.expiration_time<=time.time()-60:
    g.refresh()
    print("refresh")

url="https://www.googleapis.com/youtube/v3/playlistItems"

header={
    "Authorization":"Bearer "+g.access_token
}
params={
    "part":"contentDetails",
    "playlistId":"LL",
    "maxResults":10
}

r=requests.request("get",url,params=params,headers=header)
print(r.status_code)
print(r.text)