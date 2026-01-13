from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from fastapi.responses import JSONResponse

def register_exception_handlers(app: FastAPI):

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={"detail": "Переданы некорректные данные для этого эндпоинта"}
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        status_code = exc.status_code
        if status_code == 404:
            detail = "Данный эндпоинт не найден"
        elif status_code == 405:
            detail = "Данный эндпоинт доступен только для POST запросов"
        else:
            detail = exc.detail

        return JSONResponse(
            status_code=status_code,
            content={"detail": detail}
        )