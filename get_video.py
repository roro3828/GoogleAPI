import json
import requests
import time
import re

import googleapi


g=googleapi.GoogleAPI()
g.read_client_ids()
g.read_keys()

if g.expiration_time<=time.time()-60:
    print(g.refresh().text)
    print("refresh")
    g.save_keys()

url="https://www.googleapis.com/youtube/v3/videos"

header={
    "Authorization":"Bearer "+g.access_token
}

part="id,snippet,contentDetails,liveStreamingDetails,player,recordingDetails,statistics,status,topicDetails"
params={
    "part":"contentDetails",
    "id":"yob2y6tI134"
}

r=requests.request("get",url,params=params,headers=header)
print(r.status_code)
print(r.text)

print(re.match(r"PT((\d+)M)?((\d+)S)?","PT4M10S").groups())