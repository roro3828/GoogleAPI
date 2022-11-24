import base64
import hashlib
import requests
import os
import json
from urllib import parse
import re
import sys
from time import time

class GoogleAPI():
    def __init__(self,client_id:str=None,client_secret:str=None,app_name:str=None,access_token:str=None,refresh_token:str=None,scopes:str=None,key_path:str="keys.json",redirect_uri:str="http://localhost:8080")->None:
        self.client_id=client_id
        self.client_secret=client_secret
        self.app_name=app_name
        self.redirect_uri=redirect_uri
        self.access_token=access_token
        self.refresh_token=refresh_token
        self.scopes=scopes
        self.key_path=key_path

        self.expiration_time:float=0.0

    def generate_authorization_url(self)->str:
        authorize_url="https://accounts.google.com/o/oauth2/auth"
        params={
            "response_type":"code",
            "access_type":"offline",
            "client_id":self.client_id,
            "redirect_uri":self.redirect_uri,
            "scope":self.scopes
        }
        q=parse.urlencode(params,quote_via=parse.quote,safe=':/')
        return authorize_url+'?'+q

    def access_token_request(self,authorization_code:str)->requests.Response:
        token_url="https://accounts.google.com/o/oauth2/token"
        header={
            "Content-Type":"application/x-www-form-urlencoded"
        }
        params={
            "code":authorization_code,
            "client_id":self.client_id,
            "client_secret":self.client_secret,
            "redirect_uri":self.redirect_uri,
            "grant_type":"authorization_code"
        }
        response=requests.request(method="post",headers=header,url=token_url,params=params)

        if response.status_code==200:
            json_response=json.loads(response.text)
            self.access_token=json_response["access_token"]
            self.expiration_time=time()+float(json_response["expires_in"])
            self.refresh_token=json_response["refresh_token"]

        return response

    def refresh(self)->requests.Response:
        token_url="https://accounts.google.com/o/oauth2/token"
        header={
            "Content-Type":"application/x-www-form-urlencoded"
        }
        params={
            "refresh_token":self.refresh_token,
            "client_id":self.client_id,
            "client_secret":self.client_secret,
            "grant_type":"refresh_token"
        }
        response=requests.request(method="post",headers=header,params=params,url=token_url)

        if response.status_code==200:
            json_response=json.loads(response.text)
            self.access_token=json_response["access_token"]
            self.expiration_time=time()+float(json_response["expires_in"])

        return response
    
    def save_keys(self,path:str=None)->None:
        if path==None:
            path=self.key_path

        data={
            "app_name":self.app_name,
            "access_token":self.access_token,
            "refresh_token":self.refresh_token,
            "scopes":self.scopes,
            "expiration_time":self.expiration_time
        }

        with open(path,"w",encoding="utf-8") as f:
            json.dump(data,f,indent=4,ensure_ascii=False)

    def read_keys(self,path:str=None)->dict:
        if path==None:
            path=self.key_path

        with open(path,"r",encoding="utf-8") as f:
            data=json.load(f)

        self.app_name=data["app_name"]
        self.access_token=data["access_token"]
        self.refresh_token=data["refresh_token"]
        self.scopes=data["scopes"]
        self.expiration_time=data["expiration_time"]

        return data