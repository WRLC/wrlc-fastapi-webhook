"""
FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python
type hints.
"""
import json
import logging
import os
import secrets
from typing import Annotated

import fastapi
from fastapi import FastAPI, status, Depends, HTTPException, Request
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
    correct_username = os.getenv("USERNAME")  # Get the correct username
    if not correct_username:  # If the correct username is not present
        logging.error("Error: Correct username not set")  # Log the error
        raise HTTPException(  # Raise an exception
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,  # Internal server error status code
            detail="Correct username not set",  # Error message
        )
    correct_username_encoded = correct_username.encode()  # Encode the correct username
    is_correct_user = secrets.compare_digest(current_username, correct_username_encoded)  # Compare the usernames

    current_password = credentials.password.encode()  # Get the submitted password
    correct_password = os.getenv("PASSWORD")  # Get the correct password
    if not correct_password:  # If the correct password is not present
        logging.error("Error: Correct password not set")
        raise HTTPException(  # Raise an exception
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,  # Internal server error status code
            detail="Correct password not set",  # Error message
        )
    correct_password_encoded = correct_password.encode()  # Encode the correct password
    is_correct_pwd = secrets.compare_digest(current_password, correct_password_encoded)  # Compare the passwords

    if not (is_correct_user and is_correct_pwd):  # If the username or password is incorrect
        logging.error("Error: Incorrect email or password")  # Log the error
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
    return Response(status="success", data={"message": "Hello, World!"})


@app.post("/email", status_code=status.HTTP_201_CREATED, response_model=Response)
async def send_email(message: Message, username: Annotated[str, Depends(authenticate)]) -> Response:
    """
    Send email endpoint

    :param message: Message
    :param username: str
    :return:
    """
    if not username:  # If the username is not present
        logging.error("Error: Incorrect email or password")  # Log the error
        raise HTTPException(  # Raise an exception
            status_code=status.HTTP_401_UNAUTHORIZED,  # Unauthorized
            detail="Incorrect email or password",  # Error message
            headers={"WWW-Authenticate": "Basic"},  # Authenticate
        )

    msg = message.construct_email()  # Construct the email

    try:
        message.send_email(msg)  # Send the email
    except Exception as e:  # Handle exceptions
        logging.error("Error: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error sending email: {str(e)}",  # Error message
        ) from e

    return Response(status="success", data={"message": f"Email sent to {message.to}"})


@app.get("/alma", status_code=status.HTTP_200_OK, response_model=Response)
async def alma_challenge(challenge: str) -> Response:
    """
    Alma challenge endpoint

    :param challenge: str
    :return:
    """
    if not challenge:
        logging.error("Error: Challenge not provided")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Challenge not provided",
        )
    logging.info("Challenge: %s", challenge)
    return Response(status="success", data={"challenge": challenge})


@app.post("/alma", status_code=status.HTTP_200_OK)
async def alma_item(request: Request) -> fastapi.Response:
    """
    Alma item endpoint

    :param request: Request
    :return:
    """
    if not request:
        logging.error("Error: Item not provided")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not provided",
        )
    logging.info("Item: %s", request.json())
    return fastapi.Response()
