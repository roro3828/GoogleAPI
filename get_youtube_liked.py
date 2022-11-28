import json
import requests
import time

import googleapi


g=googleapi.GoogleAPI()
g.read_client_ids()
g.read_keys()

if g.expiration_time<=time.time()-60:
    g.refresh()
    print("refresh")

url="https://www.googleapis.com/youtube/v3/playlistItems"

header={
    "Authorization":"Bearer "+g.access_token
}
params={
    "part":"contentDetails.duration",
    "playlistId":"LL",
    "maxResults":10
}

r=requests.request("get",url,params=params,headers=header)
print(r.status_code)
print(r.text)