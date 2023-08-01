import os
import urllib.request

import json
import pandas as pd
from fastapi import APIRouter
from flask import Flask, request, jsonify
from dotenv import load_dotenv

app = Flask(__name__)

crawl_blog_router = APIRouter()


def getresult(client_id, client_secret, query, display=10, start=1, sort='sim'):
    encText = urllib.parse.quote(query)
    url = "https://openapi.naver.com/v1/search/blog?query=" + encText + \
          "&display" + str(display) + "&start" + str(start) + "&sort" + sort
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if (rescode == 200):
        response_body = response.read()
        response_json = json.loads(response_body)
    else:
        print("Error Code:" + rescode)

    return pd.DataFrame(response_json['items'])


import configparser

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, "../.env"))
# config = configparser.ConfigParser()
# config.read('./naver_search_api.ini')
client_id = os.environ["CLIENT_ID"]
# config['DEFAULT']['client_id']
client_secret = os.environ["CLIENT_SECRET"]
# config['DEFAULT']['client_secret']

display = 10
start = 1
sort = 'sim'
result_all = pd.DataFrame()

from pydantic import BaseModel
class RequestQuery(BaseModel):
    placeName: str


@crawl_blog_router.get("/api/crawl-blog")
async def crawl_blog_router1(placeName: str):
    query = placeName
    print(query)
    # return result_all
    # for i in range(0, 2):
    #     start = 1 + 100 * i
    result = getresult(client_id, client_secret, query, display, start, sort)
    for i in ["title", "description"]:
        for j in range(len(result.values)):
            result[i][j] = result[i][j].replace("<b>", "").replace("</b>", "").replace("&quot;", "").replace("&lt;", "").replace("&gt;", "")
    # print(result.replace({"<b>" : " ","</b>": " "}))
    return result
    # result_all = pd.concat([result_all, result])
    # return jsonify(result_all)
