"""
FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python
type hints.
"""
import os
import secrets
from typing import Annotated
from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from models.message import Message
from models.reponse import Response

app = FastAPI()

security = HTTPBasic()


def authenticate(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    """
    Get the current username after authenticating

    :param credentials: HTTPBasicCredentials
    :return: str
    """
    current_username = credentials.username.encode()  # Get the submitted username
    correct_username = os.getenv("USERNAME").encode()  # Get the correct username
    is_correct_user = secrets.compare_digest(current_username, correct_username)  # Compare the usernames

    current_password = credentials.password.encode()  # Get the submitted password
    correct_password = os.getenv("PASSWORD").encode()  # Get the correct password
    is_correct_pwd = secrets.compare_digest(current_password, correct_password)  # Compare the passwords

    if not (is_correct_user and is_correct_pwd):  # If the username or password is incorrect
        raise HTTPException(  # Raise an exception
            status_code=status.HTTP_401_UNAUTHORIZED,  # Unauthorized status code
            detail="Incorrect email or password",  # Error message
            headers={"WWW-Authenticate": "Basic"},  # Authenticate
        )

    return credentials.username  # Return the username


@app.get("/")
async def root():
    """
    Root endpoint

    :return:
    """
    return {
        "status": "success",
        "data": {
            "message": "Hello, World!"
        }
    }


@app.post("/email", status_code=status.HTTP_201_CREATED, response_model=Response)
async def send_email(message: Message, username: Annotated[str, Depends(authenticate)]) -> Response:
    """
    Send email endpoint

    :param message: Message
    :param username: str
    :return:
    """
    if not username:  # If the username is not present
        raise HTTPException(  # Raise an exception
            status_code=status.HTTP_401_UNAUTHORIZED,  # Unauthorized
            detail="Incorrect email or password",  # Error message
            headers={"WWW-Authenticate": "Basic"},  # Authenticate
        )

    message.construct_email()  # Construct the email

    return Response(status="success", data={"message": f"Email sent to {message.to}"})

