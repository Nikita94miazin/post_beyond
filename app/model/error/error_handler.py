from typing import Callable, Optional

from starlette.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.model.error.custom_error import CustomError
from app.model.error.error import Error


class ErrorHandler:

    @classmethod
    def value(cls, _, exception: ValueError) -> JSONResponse:
        return JSONResponse(
            status_code=420,
            content=exception.__dict__ if exception.__dict__ else Error.internal_error.__dict__
        )

    @classmethod
    def construct_handler(cls, exception: CustomError) -> Callable:
        def handler(*args) -> JSONResponse:
            return JSONResponse(
                status_code=420,
                content=exception.__dict__
            )
        return handler

    @classmethod
    def validation(cls, _, exception: RequestValidationError) -> JSONResponse:
        validation_error: CustomError = cls.extract_custom_error(exception)
        return JSONResponse(
            status_code=420,
            content=validation_error.__dict__
            if validation_error
            else Error.incorrect_params_format.__dict__
        )

    @classmethod
    def extract_custom_error(cls, exc: Exception) -> Optional[CustomError]:
        if hasattr(exc, "raw_errors") and len(exc.raw_errors) and hasattr(exc.raw_errors[0], "exc"):
            if type(exc.raw_errors[0].exc) == CustomError:
                return exc.raw_errors[0].exc
            return cls.extract_custom_error(exc.raw_errors[0].exc)

        return None
