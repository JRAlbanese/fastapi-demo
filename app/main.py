#!/usr/bin/env python3

from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import json
import os
import MySQLdb
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static", html = True), name="static")

# db config stuff
DBHOST = os.environ.get('DBHOST')
DBUSER = os.environ.get('DBUSER')
DBPASS = os.environ.get('DBPASS')
DB = "pwg2gq"

@app.get("/")  # zone apex
def zone_apex():
    return {"Hello": "Hello API", "album_endpoint":"/albums","static_endpoint":"/static"}


@app.get("/samestatement")
def thiswillreturnthesamethingalways():
    return {"This will": "always be the same"}

@app.get("/albums")
def get_albums():
        db = MySQLdb.connect(host=DBHOST, user=DBUSER, passwd=DBPASS, db=DB)
        c = db.cursor(MySQLdb.cursors.DictCursor)
        #dictcursor means that and therefor returns data arrays as dictionaries
        c.execute("""SELECT * FROM albums ORDER BY name""")
        results = c.fetchall()
        db.close() #this closes the connection, so that if we modify the database, and re-run, we will see the updated data
        return results
    #sql here selects all rows from our albums table and orders them alphabetically by name
    #the triple quotes is not needed, regular is fine



#as per the data project 1 guidelines, here is a slightly altered version of the previous function:
@app.get("/albums/{id}")
def get_one_album(id):
        db = MySQLdb.connect(host=DBHOST, user=DBUSER, passwd=DBPASS, db=DB)
        c = db.cursor(MySQLdb.cursors.DictCursor)
        c.execute("SELECT * FROM albums WHERE id=" + id)  #THIS LINE IS PARTICULARLY DIFFERENT THAN THE PREVIOUS FUNCTION
        results = c.fetchall()
        db.close() 
        return results


