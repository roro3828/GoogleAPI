import json
import requests
import time
import yt_dlp
import sys

import googleapi

g=googleapi.GoogleAPI()
g.read_client_ids("youtube-client.json")
g.read_keys()

if g.expiration_time<=time.time()-60:
    g.refresh()
    print("refresh")

ydl_opts={
    "outtmpl":r"downloads\%(title)s.%(ext)s",
    "cookiefile":None,
    "writethumbnail":True,
    "postprocessors":[
        {
            "key": "EmbedThumbnail"
        }
    ],
    "format":"bestvideo[ext!=webm]+bestaudio[ext!=webm]"
}

url="https://www.googleapis.com/youtube/v3/playlistItems"

header={
    "Authorization":"Bearer "+g.access_token
}
params={
    "part":"contentDetails",
    "playlistId":"LL",
    "maxResults":5
}

r=requests.request("get",url,params=params,headers=header)
print(r.status_code)
if r.status_code==200:
    data=json.loads(r.text)
    for i in data["items"]:
        vid=i["contentDetails"]["videoId"]
        print(vid)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(vid)