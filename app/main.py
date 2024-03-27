#!/usr/bin/env python3

from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from models import Item, Album
import json
import requests
import boto3

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# The URL for this API has a /docs endpoint that lets you see and test
# your various endpoints/methods.

@app.get("/")  # zone apex
def zone_apex():
    return {"Hello": "Hello World"}

albums = [
  {
    "name":"OK Computer",
    "artist":"Radiohead",
    "genre":"rock",
    "year":1997
  },
  {
    "name":"More Songs About Buildings and Food",
    "artist":"Talking Heads",
    "genre":"rock",
    "year":1978
  },
  {
    "name":"The Joshua Tree",
    "artist":"U2",
    "genre":"rock",
    "year":1987
  },
]

@app.get("/albums")  # zone apex
def get_albums():
    return albums

@app.post("/submit")
def submit_them(album: Album):
    return {"artist": album.artist, "band": album.title}

# Start using the "Item" BaseModel
# Post / Delete / Patch methods
@app.post("/items/{item_id}")
def add_item(item_id: int, item: Item):
    return {"item_id": item_id, "item_name": item.name}

@app.delete("/items/{item_id}")
def delete_item(item_id: int, item: Item):
    return {"action": "deleted", "item_id": item_id}

@app.patch("/items/{item_id}")
def patch_item(item_id: int, item: Item):
    return {"action": "patch", "item_id": item_id}


# api calls within an api!
@app.get("/github/repos/{user}")
def github_user_repos(user):
    url = "https://api.github.com/users/" + user + "/repos"
    response = requests.get(url)
    body = json.loads(response.text)
    return {"repos": body}

# Incorporate with boto3: simpler than the `requests` library:
@app.get("/aws/s3")
def fetch_buckets():
    s3 = boto3.client("s3")
    response = s3.list_buckets()
    buckets = response['Buckets']
    return {"buckets": buckets}
