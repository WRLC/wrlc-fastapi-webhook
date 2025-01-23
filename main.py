"""
FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python
type hints.
"""
from fastapi import FastAPI
from starlette.responses import JSONResponse
from models.message import Message
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
async def send_email(message: Message) -> JSONResponse:
    """
    Send email endpoint

    :param message: Message
    :return:
    """
    msg = message.construct_email()

    return JSONResponse(
        content={
            "status": "success",
            "data": {
                "message": "Email sent successfully",
                "subject": msg,
            }
        }
    )
