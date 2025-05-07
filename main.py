from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import user_utils as utils
import re

app = FastAPI()

class LoginRequest(BaseModel):
    info: str #either username or email
    password: str

class signupRequest(BaseModel):
    username: str
    email: str
    password: str

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=FileResponse)
def root():
    return FileResponse("static/login.html")

@app.post("/login")
async def login(login_request: LoginRequest):
    # handle empty input in backend (if someone uses tool to run api directly)
    if not login_request.password: #if empty string, this will be false
        raise HTTPException(status_code=400, detail="Password is required")
    if not login_request.info:
        raise HTTPException(status_code=400, detail="Username or email is required")

    # validation ... (uses code 400 to properly deny request)
    if not utils.isUserExist(login_request.info, login_request.password):
        raise HTTPException(status_code=400, detail="User not found. Either username, email or password is incorrect")
    return {"message": "Login successful"}

@app.post("/signup")
async def signup(signup_request: signupRequest):
    # handle empty input in backend (if someone uses tool to run api directly)
    if not signup_request.password:
        raise HTTPException(status_code=400, detail="Password is required")
    if not signup_request.username:
        raise HTTPException(status_code=400, detail="Username is required")
    if not signup_request.email:
        raise HTTPException(status_code=400, detail="Email is required")
    
    #name, email max length = 50; password max length = 60
    #valid email example: a@hu.edu.vn; google@gmail.com
    if len(signup_request.username) > 50:
        raise HTTPException(status_code=400, detail="Username must be less than 50 characters")
    if len(signup_request.email) > 50:
        raise HTTPException(status_code=400, detail="Email must be less than 50 characters")
    if not isEmailValid(signup_request.email):
        raise HTTPException(status_code=400, detail="Invalid email")
    if len(signup_request.password) > 60:
        raise HTTPException(status_code=400, detail="Password must be less than 60 characters")
    
    utils.insertUser(signup_request.username, signup_request.email, signup_request.password)
    return {"message": "Signup successful. Please return to log in screen to actually log in"}

def isEmailValid(email:str):
    x = re.search(r'^[\w\.-]+@([\w-]+\.)+[\w-]{2,4}$', email) #use regex to check if email is valid
    return bool(x)

if __name__ == "__main__":
    # import uvicorn
    # uvicorn.run(app, host="127.0.0.1", port=8000)
    pass