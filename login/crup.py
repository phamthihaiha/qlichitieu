from  fastapi import FastAPI
import model, schemas
app=fastapi()
fake_db={}
@app.post("/user/")
def create_user()       
     
     


