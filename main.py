"""
FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python
type hints.
"""
from fastapi import FastAPI
from starlette.responses import JSONResponse

from Models.Email import Email
app = FastAPI()


@app.get("/")
async def root() -> JSONResponse:
    """
    Root endpoint

    :return:
    """
    return JSONResponse(
        content={
            "status": "success",
            "data": {
                "message": "Hello, World!"
            }
        }
    )


@app.post("/email")
async def send_email(email: Email) -> JSONResponse:
    """
    Send email endpoint

    :param email: Email
    :return:
    """
    msg = email.construct_email()
    email.send(msg)

    return JSONResponse(
        content={
            "status": "success",
            "data": {
                "message": "Email sent successfully",
            }
        }
    )
