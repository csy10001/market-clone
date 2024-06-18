
from fastapi import FastAPI,UploadFile,Form
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from typing import Annotated
import sqlite3

con = sqlite3.connect('db.db', check_same_thread=False)
cur = con.cursor()

app = FastAPI() 

@app.post('/items')
async def create_item(image:UploadFile, 
                title:Annotated[str,Form()], 
                price:Annotated[int, Form()], 
                description:Annotated[str,Form()], 
                place:Annotated[str,Form()]
                ):
    
    image_bytes = await image.read()
    cur.execute(f"""
                INSERT INTO items(title,image,price,description,place)
                VALUES ('{title}','{image_bytes.hex()}',{price},'{description}','{place}')
                """)
    con.commit()
    
    return '200'

@app.post('/signup')   
def signup(id:Annotated[str,Form()], 
           password:Annotated[str,Form()],
           name:Annotated[str,Form()],
           email:Annotated[str,Form()]):
    cur.execute(f"""
                INSERT INTO users(id,name,email,password)
                VALUES ('{id}','{name}','{email}','{password}')
                """)
    con.commit()
    print(id, password)
    return '200'

@app.get('/items')
async def get_items():
    con.row_factory = sqlite3.Row
    cor = con.cursor()
    rows = cur.execute(f"""
                       SELECT * from items;
                       """).fetchall()
    
    return JSONResponse(jsonable_encoder(dict(rows) for row in rows))


app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
