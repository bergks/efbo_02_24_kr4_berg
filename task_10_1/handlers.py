from fastapi import Request
from fastapi.responses import JSONResponse
from exception import CustomExceptionA, CustomExceptionB
from models import ErrorResponse


async def custom_a_handler(request: Request, exc: CustomExceptionA):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            status_code=exc.status_code,
            message=exc.message,
            error_type="CustomExceptionA"
        ).model_dump()
    )


async def custom_b_handler(request: Request, exc: CustomExceptionB):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            status_code=exc.status_code,
            message=exc.message,
            error_type="CustomExceptionB"
        ).model_dump()
    )